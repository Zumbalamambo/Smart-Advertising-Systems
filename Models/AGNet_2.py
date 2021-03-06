from keras.models import Sequential, load_model
from keras.layers import Conv2D, MaxPooling2D, Dense, Dropout, AveragePooling2D, Flatten, BatchNormalization, ZeroPadding2D, Convolution2D, Merge
from keras.callbacks import ModelCheckpoint, TensorBoard
from keras.optimizers import SGD
import AGNetConfig
import os
from keras.applications.vgg16 import VGG16
from keras import Model
from keras.preprocessing.image import ImageDataGenerator
import tensorflow as tf

class AGNet():
    # pass

    def __init__(self):
        if not os.path.isdir(AGNetConfig.props['MODEL_PATH']):
            os.mkdir(AGNetConfig.props['MODEL_PATH'])
        
        if not os.path.isdir(AGNetConfig.props['LOG_PATH']):
            os.mkdir(AGNetConfig.props['LOG_PATH'])
        
        model_checkpoint_name = os.path.join(AGNetConfig.props['MODEL_PATH'], AGNetConfig.props['WEIGHT_NAME'])

        self._model_checkpoint = ModelCheckpoint(filepath=model_checkpoint_name, 
                                                monitor='val_loss', 
                                                verbose=1, 
                                                save_best_only=True)
        self._tensor_board = TensorBoard(log_dir=AGNetConfig.props['LOG_PATH'], 
                                        histogram_freq=0, 
                                        write_graph=True, 
                                        write_images=True)
        self._callback_list = [self._model_checkpoint, self._tensor_board]


    def __PT_model__(self):
        """VGG 16 Model 
        Parameters:
        img_rows, img_cols - resolution of inputs
        channel - 1 for grayscale, 3 for color 
        num_classes - number of categories for our classification task
        """
        (channel, img_rows, img_cols) = (3, 64, 64)
        num_classes = 6

        model = Sequential()
        model.add(Conv2D(filters = 96, kernel_size = (5,5), padding = 'same', activation = 'relu'))
        model.add(MaxPooling2D((2,2), strides = (2,2))
        model.add(Conv2D(filters = 128, kernel_size =(3, 3), padding = 'same', activation = 'relu'))
        model.add(MaxPooling2D((2,2),strides = (2,2))
        model.add(BatchNormalization)

        model.add(Conv2D(filters = 384, kernel_size = (3, 3), padding = 'same', activation = 'relu'))
        model.add(Conv2D(filters = 384, kernel_size = (3, 3), padding = 'same', activation = 'relu'))
        
        model.add(Conv2D(filters = 256, kernel_size = (3, 3), padding = 'same', activation = 'relu'))

        model.add(Flatten())
        model.add(Dense(4096, activation = 'relu'))
        model.add(Dropout(0.2))
        model.add(Dense(4096, activation = 'relu'))
        model.add(Dropout(0.2))

        # Loads ImageNet pre-trained data
        # model.load_weights('/home/vmc/vgg16_weights_tf_dim_ordering_tf_kernels_notop.h5')

        # Truncate and replace softmax layer for transfer learning
        # Add Fully Connected Layer
        # model.add(Dense(4096, activation='relu'))
        # model.add(Dropout(0.2))
        # model.layers.pop()
        # model.outputs = [model.layers[-1].output]
        # model.layers[-1].outbound_nodes = []
        model.add(Dense(num_classes, activation='sigmoid'))

        print(model.summary())

        # Uncomment below to set the first 10 layers to non-trainable (weights will not be updated)
        # for layer in model.layers[:10]:
        #     layer.trainable = True

        # Learning rate is changed to 0.001
        sgd = SGD(lr=1e-2, decay=1e-6, momentum=0.9, nesterov=True)
        model.compile(optimizer=sgd, loss='binary_crossentropy', metrics=['accuracy'])

        return model


    def train(self, X_train, y_train, X_dev, y_dev):
        # self._model = load_model('./AGNet_weights_1-improvement-30-0.22-0.90.hdf5')
        # self._model = self.__reference__()

        config = tf.ConfigProto()
        config.gpu_options.allow_growth = True
        sess = tf.Session(config = config)
        self._model = self.__vgg16_model__()
        self._model.load_weights('./AGNet_weights_1-improvement-30-0.22-0.90.hdf5')
        # for layer in self._model.layers[:10]:
        #     layer.trainable = True

        # self._model.compile(optimizer='Adam', loss='binary_crossentropy', metrics=['accuracy'])

        self._model.fit(x=X_train, y=y_train, batch_size=AGNetConfig.props['BATCH_SIZE'], 
                                epochs=AGNetConfig.props['EPOCHS'],
                                validation_data=(X_dev, y_dev),
                                callbacks=self._callback_list)


    def __evaluate__(self):
        pass


    