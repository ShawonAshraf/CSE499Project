# Instructions for BasicClassifier

## Create the anaconda env using the requirement files
Choose the file that matches your OS. However I've found Windows to be troublesome since Tensorflow doesn't provide any support at all for Windows.

### Creating ENV
- Basic syntax to create env is 

` conda create --name <env_name> <python_version> <package_list>`

- We are using    `python=3.5.2`
- So just use the requirements files. Example -

#### For macOS :

`conda create --name cse499 --file requirements_macos64.txt`

#### For Linux (Ubuntu, Mint, Fedora .... must be 64 bit) :

`conda create --name cse499 --file requirements_linux64.txt`

- Hit enter, let it download and create the env.
- Then activate it with `source activate cse499`

## Running the Classifier

- We are using 'Transferred Learning' from Google Inception Model. As a result we need to download the inception model first. You don't need to do that manually. It'll be handled by `train.sh` script.

- But before that you need to download training data. You can download it from here : http://bit.ly/2sL1t3I

- After downloading extract and copy the img_data folder inside the BasicClassifer Directory.

- Then, run `train.sh` using `./train.sh`
- Let it train. Will take a few minutes depending on the speed of your machine. *If you have Nvidia GPU with CUDA cores, it'll be faster.*

- After training is done, test with a random mango image, currently it can detect ripe and green mangoes.

- So download any mango image from internet. Copy it's path, then do the following :

`python label_image.py <your_img_path>` 

- It will show a score and the category.
