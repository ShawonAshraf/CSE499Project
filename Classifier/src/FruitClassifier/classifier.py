import os, inspect
import tensorflow as tf

from matplotlib import pyplot as plt
from matplotlib import image as mat_img

import traceback


class Classifier:
    def __init__(self, img_path, label_path, graph_path):
        # set tensorflow log level
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

        self.img_path = img_path
        self.image_name = os.path.split(self.img_path)[-1]
        self.label_path = label_path
        self.graph_path = graph_path

    def __str__(self):
        return 'Image Classifier : {}'.format(type(self))

    def __get_max_confidence_score__(self, score_dict):
        # get the dictionary and find the max confidence score
        max_score_key = max(score_dict, key=lambda k: score_dict[k])
        max_score_tuple = (max_score_key, score_dict[max_score_key])

        return max_score_tuple

    def classify_fruit(self):
        try:
            # read in image data
            image_data = tf.gfile.FastGFile(self.img_path, 'rb').read()

            # load labels
            label_lines = [line.rstrip() for line
                           in tf.gfile.FastGFile(self.label_path)]

            # graph from file
            graph_file = tf.gfile.FastGFile(self.graph_path, 'rb')

            graph_def = tf.GraphDef()
            graph_def.ParseFromString(graph_file.read())
            tf.import_graph_def(graph_def, name='')

            # create tf session

            sess = tf.Session()
            softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

            predictions = sess.run(softmax_tensor, {'DecodeJpeg/contents:0': image_data})

            # sorts the result in descending order
            top_predict = predictions[0].argsort()[-len(predictions[0]):][::-1]

            # print('Result for {} :\n'.format(self.image_name))
            # node_id = 4  # gets the best result since it's sorted
            #
            # label_string = label_lines[node_id]
            # confidence_score = predictions[0][node_id]
            #
            # print('Label : {}\t Score : {}\n\n'.format(label_string, confidence_score))

            score_dict = {}
            for node_id in top_predict:
                label_string = label_lines[node_id]
                confidence_score = predictions[0][node_id]

                # add to score_dict as key value pair
                score_dict[label_string] = confidence_score

            # call __get_max_confidence_score__ here
            max_score_tuple = self.__get_max_confidence_score__(score_dict)

            return max_score_tuple

        except Exception:
            traceback.print_exc()

    # plots the image using matplotlib
    def plot_img(self):
        image = mat_img.imread(self.img_path)
        plt.axis('off')
        plt.imshow(image)
        plt.show()

# test

# img_path = '../../img_test/green_mangoes.jpg'
# cls = Classifier(img_path)
#
# fruit, score = cls.classify_fruit()
# print('Result for image = {}: \n'.format(cls.image_name))
# print('Fruit : {}\nConfidence Score : {}\n\n'.format(fruit, score))
