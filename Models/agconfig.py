''' This is configuration for Smart Ads System
    
'''
# import sys

# sys.path.append('..')
# sys.path.append('./Models/')
# Input layer
IMAGE_WIDTH = 64
IMAGE_HEIGHT = 64
IMAGE_DEPTH = 3

# Last layer
OUTPUT_GENDER = 1
OUTPUT_AGE = 5

# Pretrain Model
WEIGHT_PATH = '/mnt/Data/MegaSyns/Projects/Smart-Advertising-Systems/train-weights-model-lastest.h5'
MODEL_ARCHITECTURE_JSON = '/mnt/Data/MegaSyns/Projects/Smart-Advertising-Systems/model_archi.json'

''' Face Detection Method
        DLIB: HOG and SVM
            Histogram of the Gradient and Support Vector Machine
        
        HAAR: HAAR METHOD
'''
DETECTION_METHOD = 'HAAR' # DLIB or HAAR

HAAR_MODEL_PATH = '/home/vmc/Desktop/Smart-Advertising-Systems/Models/haarcascade_frontalface_default.xml'

NUM_IMG_STORED = 15