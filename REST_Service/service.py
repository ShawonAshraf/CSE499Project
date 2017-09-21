"""
REST API v1_0
Supply the image as a file in a PUT request
with content-type as multipart/form-data

the response comes as a json object that will need
some parsing to show properly on mobile app. Both Android and
iOS SDK have that.

To save precious storage, the server will delete input
images as soon as it's done processing
"""



from flask import Flask, request, Response
from flask_uploads import IMAGES, UploadSet, configure_uploads
import jsonpickle

import os
import traceback
import tensorflow as tf


# classifier
class Classifier:
    def __init__(self, img_path, label_path, graph_path):
        # set tensorflow log level
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

        self.img_path = img_path
        # self.image_name = os.path.split(self.img_path)[-1]
        self.label_path = label_path
        self.graph_path = graph_path

    def __str__(self):
        return 'Image Classifier : {}'.format(type(self))

    def __get_max_confidence_score__(self, score_dict):
        # get the dictionary and find the max confidence score
        max_score_key = max(score_dict, key=lambda k: score_dict[k])
        max_score_tuple = (max_score_key, score_dict[max_score_key])

        return max_score_tuple

    def classify(self):
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

            # pass the image for predictive analysis
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


app = Flask(__name__)
# configure file storage access
app.config["UPLOADED_IMAGE_DEST"] = "temp_storage/"
image = UploadSet('image', IMAGES)
configure_uploads(app, (image,))


@app.route('/api/v1_0', methods=["PUT"])
def fruit_predict():
    # define graph and label path
    graphPath = "static/graphs/retrained_graph.pb"
    labelPath = "static/graphs/retrained_labels.txt"

    r = request
    try:
        # save the image
        imageFile = image.save(r.files["image"])
        imageURL = image.path(imageFile)

        # now run classifier
        clf = Classifier(img_path=imageURL, graph_path=graphPath, label_path=labelPath)
        result = clf.classify()

        response = {"result": "{} - {}%".format(
            result[0],
            result[1] * 100
        )}

    except Exception as e:
        response = {"result": "NULL Image, Exception : {}".format(e)}

    response_pickled = jsonpickle.encode(response)


    # remove the file, since processing is done
    os.remove(imageURL)

    # send the response
    return Response(response=response_pickled,
                    status=200,
                    mimetype="application/json")


if __name__ == '__main__':
    app.run(port=9999, debug=True)
