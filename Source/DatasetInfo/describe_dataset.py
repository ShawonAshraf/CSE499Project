import os

data_set_dir = "../img_data_v5/"

# get image categories
categories = os.listdir(data_set_dir)

print("# Dataset Version : v5")
print("#### Categories : ", categories)
print("\n#### Images per category : ")

total_images = 0
for category in categories:
    category_path = os.path.join(data_set_dir, category)
    n_images = len(os.listdir(category_path))
    total_images = total_images + n_images
    print("- Category: {}\tImages : {}".format(category, n_images))

print("\n#### Total : {}".format(total_images))
