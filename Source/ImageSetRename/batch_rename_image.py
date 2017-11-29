import os


IMAGE_ROOT_DIR = "img_data/"
IMAGE_DEST_DIR = "img_test/"

FILE_TO_REMOVE = "desktop.ini"


# get the list of sub dirs in the img_data dir
def fetch_subdirs(path):
    subdir_list = os.listdir(path)
    subdir_names = os.listdir(path)
    if FILE_TO_REMOVE in subdir_list:
        subdir_list.remove(FILE_TO_REMOVE)
    if FILE_TO_REMOVE in subdir_names:
        subdir_names.remove(FILE_TO_REMOVE)

    for i in range(len(subdir_list)):
        subdir_list[i] = path + subdir_list[i] + "/"

    return subdir_list, subdir_names


"""
    rename images in the format
    subdir_name/subdir_name_index.extension
"""


def rename_images(subdir_path, subdir_name):
    iteration_no = 1

    files_in_dir = os.listdir(subdir_path)
    if FILE_TO_REMOVE in files_in_dir:
        files_in_dir.remove(FILE_TO_REMOVE)

    print("DIR => {}\t{} IMAGES\n".format(subdir_path, len(files_in_dir)))
    for file in files_in_dir:
        _, extension = os.path.splitext(file)

        # rename
        new_name = "{}_{}{}".format(subdir_name, iteration_no, extension)
        try:
            dest_folder_name = os.path.join(IMAGE_DEST_DIR, subdir_name)

            source = os.path.join(subdir_path, file)
            dest = os.path.join(IMAGE_DEST_DIR, subdir_name, new_name)

            # create folder
            if not os.path.exists(dest_folder_name):
                os.mkdir(dest_folder_name)

            # now rename
            print("rename: {} => {}".format(source, dest))
            os.rename(source, dest)
            iteration_no = iteration_no + 1
        except FileExistsError as e:
            print("File already renamed. Skipping")



subdirs, names = fetch_subdirs(IMAGE_ROOT_DIR)

list_size = len(names) # both have same size
for i in range(list_size):
    subdir_path = subdirs[i]
    subdir_name = names[i]

    rename_images(subdir_path, subdir_name)
    print("\n")

