from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
import os


dataset_root = "img_data/train/"
preview_dir = "img_data/preview/"


datagen = ImageDataGenerator(
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode="nearest")

img = load_img(dataset_root + "fresh_apple/fresh_apple_2.jpg")
x = img_to_array(img)
x = x.reshape((1,) + x.shape)


i = 0
for batch in datagen.flow(x, batch_size=1, save_to_dir=preview_dir, save_prefix="fresh_apple", save_format="jpeg"):
    i += 1
    if i > 20:
        break


