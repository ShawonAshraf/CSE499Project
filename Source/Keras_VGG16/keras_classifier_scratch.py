from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Activation, Flatten, Dropout, Dense
from keras import losses, optimizers, metrics

# dataset dir
dataset_root = "img_data/train/"
preview_dir = "img_data/preview/"

# create generator
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



# create the model
model = Sequential()

model.add(Conv2D(32, (3,3), input_shape=(3, 150, 150)))
model.add(Activation("relu"))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(64, (3,3)))
model.add(Activation("relu"))
model.add(MaxPooling2D(pool_size=(2, 2)))

# convert 3D features to 2D features
model.add(Flatten())
model.add(Dense(64))
model.add(Activation("relu"))
model.add(Dropout(0.5))
model.add(Dense(1))
model.add(Activation("sigmoid"))

model.compile(loss=losses.mean_squared_error, optimizer=optimizers.sgd, metrics=metrics.categorical_accuracy)