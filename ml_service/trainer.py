import numpy as np
import pandas
from IPython import display
import tensorflow as tf
from ml_common import *
# Training Args
LEARNING_RATE = 500
STEPS = 500

MODEL_OUTPUT_DIR = './model/'

CSV_FILE_PATH = '''./test_new.csv'''
CSV_FILE_FORMAT = {
    'zipcode' : str,
    'longitude' : np.float32,
    'latitude' : np.float32,
    'is_for_sale' : bool,
    'property_type' : str,
    'bedroom' : np.float32,
    'bathroom' : np.float32,
    'size' : np.float32,
    'list_price' : np.float32,
    'last_update' : np.float32
}

pandas.options.display.float_format = '{:.1f}'.format

# load in the data from CSV file
property_dataframe = pandas.read_csv(CSV_FILE_PATH, dtype=CSV_FILE_FORMAT)

# Randomize the index
property_dataframe = property_dataframe.reindex(
    np.random.permutation(property_dataframe.index))

# Pick out the columns that we care about
property_dataframe = property_dataframe[COLUMNS]

# Clean up data
property_dataframe = property_dataframe[property_dataframe['list_price'] != 0]
property_dataframe = property_dataframe[property_dataframe['size'] != 0]

# Drop rows with any NaN value
property_dataframe = property_dataframe.dropna()
train_features_label = property_dataframe[FEATURE_LABEL_COLUMNS]
display.display(property_dataframe.head(10))

# Linear Regressor
linear_regressor = tf.contrib.learn.LinearRegressor(
    feature_columns=feature_columns,
    optimizer=tf.train.AdamOptimizer(learning_rate=LEARNING_RATE),
    model_dir=MODEL_OUTPUT_DIR)

print "Training model..."

    
def input_fn_train():
    return input_fn(train_features_label)

linear_regressor.fit(input_fn=input_fn_train, steps=STEPS)

print "Training Done!"
