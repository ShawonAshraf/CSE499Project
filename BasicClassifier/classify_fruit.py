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

# now testing

# empty init list
test_images = []
test_image_path = 'img_test/'

test_images = [test_image_path+x for x in os.listdir(test_image_path)]

process_list = test_images
print("Number of images in test set : {}".format(len(process_list)))


for image in process_list:
    try:
        print('Input image = {}'.format(image))
        init_time = time.time()
        # classify(image)
        print(classify(image_path=image))
        end_time = time.time()
        exec_time = end_time - init_time
        print(" in {} s\n\n".format(exec_time))
    except FileNotFoundError:
        print('{} not found\n\n'.format(image))
    except Exception as e:
        pass
