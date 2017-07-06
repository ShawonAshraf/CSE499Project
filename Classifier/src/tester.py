import os, sys, inspect

sys.path.insert(0, 'FruitClassifier')
sys.path.insert(1, 'PathGetter')
try:
    from FruitClassifier.classifier import Classifier
    from PathGetter.path_getter import get_path
except ImportError:
    print('Import Error')

# test

if __name__ == '__main__':
    img_path = get_path('../img_test/mango_001.jpg')
    label_path = get_path('../Training/retrained_labels.txt')
    graph_path = get_path('../Training/retrained_graph.pb')

    # create the classifier
    # supply the image path, training label and graph file path

    cls = Classifier(img_path, label_path, graph_path)
    fruit, score = cls.classify()

    print('Result for image = {}: \n'.format(cls.image_name))
    print('Fruit : {}\nConfidence Score : {}%\n\n'.format(fruit, score * 100))

    # plot the image using plot_img
    # cls.plot_img()
