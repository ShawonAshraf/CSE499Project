import os
import sys

import numpy as np
from PIL import Image
from keras.models import load_model

loaded_model = load_model("saved_models/bin_model_1.h5")
img_path = sys.argv[1]

labels = ["fresh", "rotten"]


# load and resize image
def prepare_image(img_path):
    image = Image.open(img_path)
    image = image.resize((150, 150))
    image_array = np.array(image)
    sample = np.array([image_array])

    return sample


img_as_array = prepare_image(img_path=img_path)

prediction = loaded_model.predict(img_as_array)
labelIndex = int(prediction[0][0])
print("{}\t is ==> {}".format(os.path.split(img_path)[-1], labels[labelIndex]))
