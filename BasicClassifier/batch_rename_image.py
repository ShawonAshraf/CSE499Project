import os


IMAGE_ROOT_DIR = "img_data/fresh_orange/"
IMAGE_DEST_DIR = "img_data/fresh_orange/"

FILE_TO_REMOVE = "desktop.ini"

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
            dest = os.path.join(IMAGE_DEST_DIR, new_name)

            # create folder
            if not os.path.exists(dest_folder_name):
                os.mkdir(dest_folder_name)

            # now rename
            print("rename: {} => {}".format(source, dest))
            os.rename(source, dest)
            iteration_no = iteration_no + 1
        except FileExistsError as e:
            print("File already renamed. Skipping")


rename_images(subdir_path=IMAGE_ROOT_DIR, subdir_name="fresh_orange")


