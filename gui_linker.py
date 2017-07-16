from Classifier.src.FruitClassifier.classifier import Classifier

import sys

# path for graph and labels and image
# all from sys args
image_path = sys.argv[1]
label = sys.argv[2]
graph = sys.argv[3]

cls = Classifier(img_path=image_path, label_path=label, graph_path=graph)
f, s = cls.classify()

print("Fruit : {}\n".format(f))