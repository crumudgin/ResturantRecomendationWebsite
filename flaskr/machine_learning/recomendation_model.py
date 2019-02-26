import numpy as np
from keras.layers import *
from keras.models import *
from keras import backend as K
import tensorflow as tf
import os

np.random.seed(1)
EMBEDING_SIZE = 32
INPUT_SIZE = 1

BN_AXIS = 3

def relu(x):
	return Activation("relu")(x)

def identity_block(x, f, filters, stage, block):
	conv_name_base = "res%d_branch" %stage
	bn_name_base = "bn%d_branch" %stage

	F1, F2, F3 = filters

	x_shortcut = x
	x = Conv2D(filters=F1, kernel_size=(1, 1), name="%s1%sa" %(conv_name_base, block))(x)
	x = BatchNormalization(axis=BN_AXIS, name="%s1%sa" %(bn_name_base, block))(x)
	x = Activation("relu")(x)

	x = Conv2D(filters=F2, kernel_size=(f, f), padding="same", name="%s2%sb" %(conv_name_base, block))(x)
	x = BatchNormalization(axis=BN_AXIS, name="%s2%sb" %(bn_name_base, block))(x)
	x = Activation("relu")(x)

	x = Conv2D(filters=F3, kernel_size=(1, 1), name="%s3%sc" %(conv_name_base, block))(x)
	x = BatchNormalization(axis=BN_AXIS, name="%s2%sc" %(bn_name_base, block))(x)

	x = Add()([x, x_shortcut])
	x = Activation("relu")(x)

	return x

def conv_block(x, kernel, filters, stage, block ,strides=(2, 2)):
	conv_name_base = "res%d_branch" %stage
	bn_name_base = "bn%d_branch" %stage

	F1, F2, F3 = filters

	x_shortcut = x
	x = Conv2D(F1, (1, 1), strides=strides, name="%s2%sa" %(block, conv_name_base, ))(x)
	x = BatchNormalization(axis=BN_AXIS, name="%s2%sa" %(block, bn_name_base, ))(x)
	x = Activation("relu")(x)

	x = Conv2D(F2, kernel, padding="same", name="%s2%sb" %(block, conv_name_base, ))(x)
	x = BatchNormalization(axis=BN_AXIS, name="%s2%sb" %(block, bn_name_base, ))(x)
	x = Activation("relu")(x)

	x = Conv2D(F3, (1, 1), name="%s2%sc" %(block, conv_name_base, ))(x)
	x = BatchNormalization(axis=BN_AXIS, name="%s2%sc" %(block, bn_name_base, ))(x)

	x_shortcut = Conv2D(F3, (1, 1), strides=strides, name="%s1%s" %(conv_name_base, block))(x_shortcut)
	x_shortcut = BatchNormalization(axis=BN_AXIS, name="%s1%s" %(bn_name_base, block))(x_shortcut)

	x = Add()([x, x_shortcut])
	x = Activation("relu")(x)

	return x

def define_model(user_dim, res_dim):
	# backend.tensorflow_backend._get_available_gpus()
	user_input = Input(shape=[1], name="user")
	resturant_input = Input(shape=[1], name="res")

	user_embeding = Embedding(output_dim=EMBEDING_SIZE, 
		input_dim=user_dim, 
		input_length=INPUT_SIZE, 
		name="user_embeding")(user_input)
	resturant_embeding = Embedding(output_dim=EMBEDING_SIZE, 
		input_dim=res_dim, 
		input_length=INPUT_SIZE, 
		name="res_embeding")(resturant_input)
	# user_embeding = Dense(EMBEDING_SIZE, activation="relu")(user_input)
	# resturant_embeding = Dense(EMBEDING_SIZE, activation="relu")(resturant_input)

	user_vec = Reshape([EMBEDING_SIZE])(user_embeding)
	res_vec = Reshape([EMBEDING_SIZE])(resturant_embeding)

	# user_dense = Dense(20, activation="relu")(user_vec)
	# res_dense = Dense(20, activation="relu")(res_vec)

	embedings_togeather = Concatenate()([user_vec, res_vec])
	dense = Dense(9408)(embedings_togeather)
	embedings_img = Reshape([56,56,3])(dense)
	padded = ZeroPadding2D((3, 3))(embedings_img)
	c1 = Conv2D(8, (7, 7), strides=(2, 2))(padded)
	batch1 = BatchNormalization(axis=3)(c1)
	a1 = Activation("relu")(batch1)
	p1 = MaxPooling2D((3, 3), strides=(2, 2))(a1)

	x = conv_block(p1, 3, [2, 2, 8], stage=2, block="a", strides=(1, 1))
	x = identity_block(x, 3, [2, 2, 8], stage=2, block="b")
	x = identity_block(x, 3, [2, 2, 8], stage=2, block="c")

	x = conv_block(x, 3, [4, 4, 16], stage=3, block="a")
	x = identity_block(x, 3, [4, 4, 16], stage=3, block="b")
	x = identity_block(x, 3, [4, 4, 16], stage=3, block="c")
	x = identity_block(x, 3, [4, 4, 16], stage=3, block="d")
	

	x = AveragePooling2D((5, 5), name="avg_pool")(x)

	x = Flatten()(x)

	out = Dense(5)(x)

	model = Model(inputs=[user_input, resturant_input], outputs=out)

	# optimizers.Adam(lr=.0001)
	model.compile(loss='binary_crossentropy',
          optimizer='adam',
          metrics=['accuracy'])
	return model

def new_model():
	print("generating new model")
	return define_model(80000, 80000)

def old_model():
	print("running on old model")
	json_file = open('model.json', 'r')
	loaded_model_json = json_file.read()
	json_file.close()
	loaded_model = model_from_json(loaded_model_json)
	# load weights into new model
	loaded_model.load_weights("model.h5")
	print("Loaded model from disk")
	loaded_model.compile(loss='binary_crossentropy',
          optimizer='adam',
          metrics=['accuracy'])
	return loaded_model

def write_model(model):
	model_json = model.to_json()
	with open("model.json", "w") as json_file:
	    json_file.write(model_json)
	# serialize weights to HDF5
	model.save_weights("model.h5")
	print("Saved model to disk")