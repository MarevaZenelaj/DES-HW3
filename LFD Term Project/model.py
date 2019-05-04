import numpy as np
import keras
import tensorflow as tf
import csv

def read_train_csv(filename):
	train_data = csv.reader(filename)
	header = train_data[0]
	print(len(header))

read_train_csv("train.csv")