# Instructions for BasicClassifier

## Create the anaconda env using the requirement files
Choose the file that matches your OS. However I've found Windows to be troublesome since Tensorflow doesn't provide any support at all for Windows.

### Installing packages

#### Packages to install : 

* numpy
* scikit-learn
* matplotlib
* jupyter
* tensorflow

Install the following packages one by one using `pip`. Before that make sure you've `python3` installed. If you're on a Linux Distro and your Distro includes both `python2` and `python3`, use `pip3` instead of `pip` 
to install `python3` pakages.

**Syntax** : `pip install <package>`

**Example** : `pip install tensorflow`



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

- You can also use `classify_fruits.py` , add the img paths in the `images` list.
