import os, sys
import tensorflow as tf
import time

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


def classify(image_path):
    # Read in the image_data
    image_data = tf.gfile.FastGFile(image_path, 'rb').read()

    # Loads label file, strips off carriage return
    label_lines = [line.rstrip() for line 
                   in tf.gfile.GFile("../Training/retrained_labels.txt")]

    # Unpersists graph from file
    with tf.gfile.FastGFile("../Training/retrained_graph.pb", 'rb') as f:
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

mango_images = [
    '../img_test/green_mangoes.jpg',
    '../img_test/green_mango_2.jpg',
    '../img_test/overripe_ataulfo_mango.png',
    '../img_test/ripe_mango_1.jpg',
    '../img_test/ripe_mango_2.jpg',
    '../img_test/rotten_mango.jpg',
    '../img_test/mango_001.jpg',
    '../img_test/Mango_Ataulfo.jpg',
    '../img_test/gvr.jpg',
]

banana_images = [
    '../img_test/banana.jpeg'
]

process_list = mango_images + banana_images

for image in process_list:
    try:
        print('Input image = {}'.format(image))
        init_time = time.time()
        classify(image)
        end_time = time.time()
        exec_time = end_time - init_time
        print(" in {} s\n\n".format(exec_time))
    except FileNotFoundError:
        print('{} not found\n\n'.format(image))
