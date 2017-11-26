import os, sys
import tensorflow as tf
from sklearn.metrics import confusion_matrix

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


def classify(image_path):
    # Read in the image_data
    image_data = tf.gfile.FastGFile(image_path, 'rb').read()

    # Loads label file, strips off carriage return
    label_lines = [line.rstrip() for line
                   in tf.gfile.GFile("retrained_labels.txt")]

    # label_names = label_lines

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

        # global_pred = predictions

        # Sort to show labels of first prediction in order of confidence
        top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
        # label_id = top_k

        print('Result for {} :\n'.format(image_path))
        # for node_id in top_k:
        #     human_string = label_lines[node_id]
        #     score = predictions[0][node_id]
        #     print('Category : {} \nScore = {} %'.format(human_string, score * 100))
        node_id = top_k[0]
        print('Category : {}\tScore : {}'.format(label_lines[node_id], predictions[0][node_id]))

        print('\nDONE===========================', end='\n')

        return label_lines, predictions[0], top_k


# get confusion matrix

def get_cnf_matrix(label, pred):
    with tf.Session() as sess:
        mat = tf.confusion_matrix(label, pred)
        print(mat)


# now testing



image_test_root_dir = 'img_test/'
test_image_list = os.listdir(image_test_root_dir)

# test for one image
test_image = os.path.join(image_test_root_dir, test_image_list[0])
l, p, k = classify(test_image)

node_id = k[0]
ground_truth_id = 5

cnf = confusion_matrix(y_true=[5], y_pred=[k[0]])
print(cnf)