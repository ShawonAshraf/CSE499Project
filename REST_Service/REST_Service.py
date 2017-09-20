from flask import Flask, abort, jsonify, request

import base64

import sys, os, inspect

sys.path.insert(0, ".")
try:
    from .classifier import Classifier as clf
except ImportError:
    pass

app = Flask(__name__)


# for decoding images from base64 string from json

def convertStrToImage(str):
    imagePath = "imSaved.jpg"

    fh = open(imagePath, "wb")
    fh.write(str.decode("base64"))
    fh.close()

    return imagePath


@app.route('/api', methods=["POST"])
def fruit_predict():
    # define graph and label path

    graphPath = "graphs/retrained_graph.pb"
    labelPath = "graphs/retrained_labels.txt"

    # get json data and check for errors
    data = request.get_json(force=True)

    # get image from json
    image = convertStrToImage(data["image"])

    # create classifier
    classifier = clf(img_path=image, graph_path=graphPath, label_path=labelPath)
    score = classifier.classify()

    # create and output object
    output = score[0]

    return jsonify(result=output)


if __name__ == '__main__':
    app.run(port=9999, debug=True)
