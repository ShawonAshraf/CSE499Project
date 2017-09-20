from flask import Flask, request, Response
import numpy as np
import cv2
import jsonpickle


app = Flask(__name__)


@app.route('/api', methods=["POST"])
def fruit_predict():
    # define graph and label path
    graphPath = "static/graphs/retrained_graph.pb"
    labelPath = "static/graphs/retrained_labels.txt"

    # get data from request
    data = np.fromstring(request.data, np.uint8)

    # decode image
    try:
        savedImagePath = "static/raw.jpg"
        decodedImage = cv2.imdecode(data, cv2.IMREAD_COLOR)
        cv2.imwrite(savedImagePath, decodedImage)

        # create the classifier
        classifier = Classifier(img_path=request.data,
                                graph_path=graphPath,
                                label_path=labelPath)
        result = classifier.classify()

        # build response dict
        response = {"result": "{} with a score of {}".format(
            result[0],
            result[1]
        )}
    except Exception as e:
        response = {"error": "ERROR!"}

    response_pickled = jsonpickle.encode(response)

    # send the response
    return Response(response=response_pickled,
                    status=200,
                    mimetype="application/json")



if __name__ == '__main__':
    app.run(port=9999, debug=True)
