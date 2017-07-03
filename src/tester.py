import os, sys, inspect

sys.path.insert(0, 'FruitClassifier')
sys.path.insert(1, 'PathGetter')
try:
    from FruitClassifier.classifier import Classifier
    from PathGetter.path_getter import get_path
except ImportError:
    print('Error')


# test

print(inspect.getfile(Classifier))
img_path = get_path('../img_test/green_mangoes.jpg')
cls = Classifier(img_path)

fruit, score = cls.classify_fruit()
print('Result for image = {}: \n'.format(cls.image_name))
print('Fruit : {}\nConfidence Score : {}\n\n'.format(fruit, score))