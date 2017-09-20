import os, sys
import tensorflow as tf
import time

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


def classify(image_path):
    # Read in the image_data
    image_data = tf.gfile.FastGFile(image_path, 'rb').read()

    # Loads label file, strips off carriage return
    label_lines = [line.rstrip() for line
                   in tf.gfile.GFile("retrained_labels.txt")]

    # Unpersists graph from file
    with tf.gfile.FastGFile("retrained_graph.pb", 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        tf.import_graph_def(graph_def, name='')

    with tf.Session() as sess:
        # Feed the image_data as input to the graph and get first prediction
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

        predictions = sess.run(softmax_tensor, \
                               {'DecodeJpeg/contents:0': image_data})

        # Sort to show labels of first prediction in order of confidence
        top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]

        print('Result for {} :\n'.format(image_path))
        for node_id in top_k:
            human_string = label_lines[node_id]
            score = predictions[0][node_id]
            print('Category : {} \nScore = {} %'.format(human_string, score * 100))

        print('\nDONE===========================', end='')


def get_labels():
    label_lines = [line.rstrip() for line
                   in tf.gfile.GFile("retrained_labels.txt")]
    return label_lines


def get_conf_matrix(image_path):
    image_data = tf.gfile.FastGFile(image_path, 'rb').read()

    # label_strings = get_labels()
    labels = [0, 1, 2, 3]

    # Unpersists graph from file
    with tf.gfile.FastGFile("retrained_graph.pb", 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        tf.import_graph_def(graph_def, name='')

    with tf.Session().as_default() as sess:
        # Feed the image_data as input to the graph and get first prediction
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

        predictions = sess.run(softmax_tensor, \
                               {'DecodeJpeg/contents:0': image_data})

        conf_matrix = tf.confusion_matrix(labels=labels, predictions=predictions[0], num_classes=len(labels))
        # print(predictions)
    return conf_matrix.get_values()


def _create_local(name, shape, collections=None, validate_shape=True,
                  dtype=tf.float32):
    """Creates a new local variable.
    Args:
      name: The name of the new or existing variable.
      shape: Shape of the new or existing variable.
      collections: A list of collection names to which the Variable will be added.
      validate_shape: Whether to validate the shape of the variable.
      dtype: Data type of the variables.
    Returns:
      The created variable.
    """
    # Make sure local variables are added to tf.GraphKeys.LOCAL_VARIABLES
    collections = list(collections or [])
    collections += [tf.GraphKeys.LOCAL_VARIABLES]
    return tf.Variable(
        initial_value=tf.zeros(shape, dtype=dtype),
        name=name,
        trainable=False,
        collections=collections,
        validate_shape=validate_shape)


# Function to aggregate confusion
def _get_streaming_metrics(prediction, label, num_classes):
    with tf.name_scope("eval"):
        batch_confusion = tf.confusion_matrix(label, prediction,
                                              num_classes=num_classes,
                                              name='batch_confusion')

        confusion = _create_local('confusion_matrix',
                                  shape=[num_classes, num_classes],
                                  dtype=tf.int32)
        # Create the update op for doing a "+=" accumulation on the batch
        confusion_update = confusion.assign(confusion + batch_confusion)
        # Cast counts to float so tf.summary.image renormalizes to [0,255]
        confusion_image = tf.reshape(tf.cast(confusion, tf.float32),
                                     [1, num_classes, num_classes, 1])

    return confusion, confusion_update  # Define the metrics:
    names_to_values, names_to_updates = slim.metrics.aggregate_metric_map({
        'Accuracy': slim.metrics.streaming_accuracy(predictions, labels),
        'Recall_5': slim.metrics.streaming_recall_at_k(
            logits, labels, 5),
        'Mean_absolute': tf.metrics.mean_absolute_error(labels,
                                                        predictions),
        'Confusion_matrix': _get_streaming_metrics(labels, predictions,
                                                   dataset.num_classes - FLAGS.labels_offset),
    })
    [confusion_matrix] = slim.evaluation.evaluate_once(
        master=FLAGS.master,
        checkpoint_path=checkpoint_path,
        logdir=FLAGS.eval_dir,
        num_evals=num_batches,
        eval_op=list(names_to_updates.values()),
        variables_to_restore=variables_to_restore,
        session_config=session_config,
        final_op=[names_to_updates['Confusion_matrix']]
    )
    print(confusion_matrix)  # now testing

mango_images = [
    'img_test/green_mangoes.jpg',
    'img_test/green_mango_2.jpg',
    'img_test/overripe_ataulfo_mango.png',
    'img_test/ripe_mango_1.jpg',
    'img_test/ripe_mango_2.jpg',
    'img_test/rotten_mango.jpg',
    'img_test/mango_001.jpg',
    'img_test/Mango_Ataulfo.jpg',
    'img_test/gvr.jpg',
]

banana_images = [
    'img_test/banana.jpeg',
    'img_test/banana_2.JPG',
]

process_list = mango_images + banana_images
print("Number of images in test set : {}".format(len(process_list)))

print(get_conf_matrix(banana_images[0]))


# for image in process_list:
#     try:
#         print('Input image = {}'.format(image))
#         init_time = time.time()
#         # classify(image)
#         print(get_conf_matrix(image_path=image))
#         end_time = time.time()
#         exec_time = end_time - init_time
#         print(" in {} s\n\n".format(exec_time))
#     except FileNotFoundError:
#         print('{} not found\n\n'.format(image))
