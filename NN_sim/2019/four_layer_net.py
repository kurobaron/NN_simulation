# coding: utf-8
import numpy as np
from layers import *
from collections import OrderedDict

class FourLayerNet:
	def __init__(self, input_size, hidden_size, output_size, weight_init_std = 0.01):
		self.params = {}
		self.params['W1'] = weight_init_std*np.random.randn(input_size, hidden_size)
		self.params['b1'] = np.zeros(hidden_size)
		self.params['W2'] = weight_init_std*np.random.randn(hidden_size, hidden_size)
		self.params['b2'] = np.zeros(hidden_size)
		self.params['W3'] = weight_init_std*np.random.randn(hidden_size, hidden_size)
		self.params['b3'] = np.zeros(hidden_size)
		self.params['W4'] = weight_init_std*np.random.randn(hidden_size, output_size)
		self.params['b4'] = np.zeros(output_size)
		self.layers = OrderedDict()
		self.layers['Affine1'] = Affine(self.params['W1'], self.params['b1'])
		self.layers['Affine2'] = Affine(self.params['W2'], self.params['b2'])
		self.layers['Affine3'] = Affine(self.params['W3'], self.params['b3'])
		self.layers['Affine4'] = Affine(self.params['W4'], self.params['b4'])
		self.lastLayer = MSELoss()

	def predict(self, x):
		for layer in self.layers.values():
			x = layer.forward(x)
		return x

	def loss(self, x, t):
		y = self.predict(x)
		return self.lastLayer.forward(y, t)

	def accuracy(self, x, t):
		y = self.predict(x)
		accuracy = np.sum(y*t)/(np.linalg.norm(y, ord=2)*np.linalg.norm(t, ord=2))
		return accuracy

	def gradient(self, x, t):
		self.loss(x, t)
		dout = 1
		dout = self.lastLayer.backward(dout)
		layers = list(self.layers.values())
		layers.reverse()
		for layer in layers:
			dout = layer.backward(dout)
		grads = {}
		grads['W1'] = self.layers['Affine1'].dW
		grads['b1'] = self.layers['Affine1'].db
		grads['W2'] = self.layers['Affine2'].dW
		grads['b2'] = self.layers['Affine2'].db
		grads['W3'] = self.layers['Affine3'].dW
		grads['b3'] = self.layers['Affine3'].db
		grads['W4'] = self.layers['Affine4'].dW
		grads['b4'] = self.layers['Affine4'].db
		return grads