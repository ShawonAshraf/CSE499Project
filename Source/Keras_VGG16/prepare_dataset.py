import os
import random
from shutil import copyfile

random.seed(42)

main_dataset_dir_root = "../img_data_v5/"
work_dataset_dir_root = "img_data/"

# get categories
categories = os.listdir(main_dataset_dir_root)
category_paths = [os.path.join(main_dataset_dir_root, path_name) for path_name in categories]

train_ratio = 0.80
validation_ratio = 0.20


# generate random indexes for train and validation set
def get_train_index(image_list, ratio=train_ratio):
    length = len(image_list)
    train_data_size = int(length * ratio)
    indices = []

    for i in range(train_data_size):
        index = random.randint(0, length - 1)
        indices.append(index)

    return indices


def get_validation_index(image_list, ratio=validation_ratio):
    length = len(image_list)
    validation_data_size = int(length * ratio)
    indices = []

    for i in range(validation_data_size):
        index = random.randint(0, length - 1)
        indices.append(index)

    return indices


"""
    create batch data. 
    index_get takes a get_index method as param according to
    batch_name = train|validation
"""


def create_batch_data(batch_name, index_get):
    for c_path in category_paths:
        images_in_path = os.listdir(c_path)
        indices = index_get(image_list=images_in_path)

        for i in indices:
            src_image_path = os.path.join(c_path, images_in_path[i])
            category_name = os.path.split(c_path)[1]
            dest_dir = os.path.join(work_dataset_dir_root, batch_name, category_name)

            # if dir doesn't exist, create it
            if not os.path.exists(dest_dir):
                os.mkdir(dest_dir)

            dest_image_path = os.path.join(dest_dir, images_in_path[i])
            copyfile(src=src_image_path, dst=dest_image_path)


# call the methods
create_batch_data(batch_name="train", index_get=get_train_index)
create_batch_data(batch_name="validation", index_get=get_validation_index)
