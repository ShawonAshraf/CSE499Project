# batch rename all the images in the dir

import os
import sys

set_name = sys.argv[1]
path = "img_data/" + set_name + "/"

fname = os.listdir(path)

print("In dir : ", path)
print("Total {} images\n\n".format(len(fname)))

print("Renaming .....\n")
image_number = 0
for f in fname:
    _, f_ext = os.path.splitext(f)

    # rename
    new_name = "newDataSet/{}.{}{}".format(set_name, image_number, f_ext)

    # if file already exists, skip
       
    try:
        os.rename(path+f, new_name)
        # print(f, "\t renamed to ==> ", new_name)
        image_number = image_number + 1
    except FileExistsError as e:
         print("File already renamed, skipping .....")
