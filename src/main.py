from .FruitClassifier.Classifier import Classifier

# test

img_path = '../../img_test/green_mangoes.jpg'
cls = Classifier(img_path)

fruit, score = cls.classify_fruit()
print('Result for image = {}: \n'.format(cls.image_name))
print('Fruit : {}\nConfidence Score : {}\n\n'.format(fruit, score))
# cls.plot_img()
