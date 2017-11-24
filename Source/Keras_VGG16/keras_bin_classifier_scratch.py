from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Activation, Flatten, Dropout, Dense
from keras import backend as K
import h5py

# dataset dir
dataset_root = "img_data/bin_class/train/"
validation_root = "img_data/bin_class/validation/"

# number of train and validation samples
n_train = int(1313 * 0.80)
n_valid = 1313 - n_train

# image dim
img_width, img_height = 150, 150

# create the model
if K.image_data_format() == 'channels_first':
    input_shape = (3, img_width, img_height)
else:
    input_shape = (img_width, img_height, 3)

model = Sequential()

# layer 1
model.add(Conv2D(32, (3, 3), input_shape=input_shape))
model.add(Activation("relu"))
model.add(MaxPooling2D(pool_size=(2, 2)))

# layer 2
model.add(Conv2D(32, (3, 3)))
model.add(Activation("relu"))
model.add(MaxPooling2D(pool_size=(2, 2)))

# layer 3
model.add(Conv2D(64, (3, 3)))
model.add(Activation("relu"))
model.add(MaxPooling2D(pool_size=(2, 2)))

# convert 3D features to 2D features
model.add(Flatten())
model.add(Dense(64))
model.add(Activation("relu"))
model.add(Dropout(0.5))
model.add(Dense(1))
model.add(Activation("sigmoid"))

model.compile(loss="binary_crossentropy", optimizer="adagrad", metrics=["accuracy"])

# data preparation
batch_size = 16

train_datagen = ImageDataGenerator(
    rescale=1. / 255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True)

test_datagen = ImageDataGenerator(rescale=1. / 255)

# generators for train and validation
train_generator = train_datagen.flow_from_directory(dataset_root, target_size=(img_width, img_height),
                                                    class_mode="binary",
                                                    batch_size=batch_size)
validation_generator = test_datagen.flow_from_directory(validation_root, target_size=(img_width, img_height),
                                                        batch_size=batch_size,
                                                        class_mode="binary")

# train
model.fit_generator(train_generator, steps_per_epoch=n_train // batch_size, epochs=50,
                    validation_data=validation_generator, validation_steps=n_valid // batch_size)
model.save_weights("saved_models/train_1_weight.h5")
model.save("saved_models/bin_model_1.h5")
