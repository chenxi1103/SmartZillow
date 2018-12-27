import numpy as np
import pandas
import tensorflow as tf

# Feature, Label, Column
COLUMNS = ['zipcode', 'longitude', 'latitude', 'is_for_sale', 'property_type', 'bedroom', 'bathroom', 'size', 'list_price', 'last_update']
CATEGORICAL_COLUMNS = ['zipcode', 'property_type']
CONTINUOUS_COLUMNS = ['bedroom', 'bathroom', 'size']
LABEL_COLUMN = 'list_price'
FEATURE_LABEL_COLUMNS = ['zipcode', 'property_type', 'bedroom', 'bathroom', 'size', 'list_price']

# Prepare features
# discrete data
zipcode = tf.contrib.layers.sparse_column_with_hash_bucket('zipcode', hash_bucket_size=1000)
property_type = tf.contrib.layers.sparse_column_with_hash_bucket('property_type', hash_bucket_size=50)

# real number
bedroom = tf.contrib.layers.real_valued_column('bedroom')
bathroom = tf.contrib.layers.real_valued_column('bathroom')
size = tf.contrib.layers.real_valued_column('size')
size_buckets = tf.contrib.layers.bucketized_column(size, boundaries=np.arange(6000, step=200).tolist())

feature_columns = [zipcode, property_type, bedroom, bathroom, size_buckets]

# input_fn return format: {feature_columns, label}
# feature_columns: (column_name : tf.constant}
# label: tf.constant
def input_fn(dataframe):
    continous_cols = {k : tf.constant(dataframe[k].values) for k in CONTINUOUS_COLUMNS}
    categorical_cols = {k : tf.SparseTensor(
            indices = [[i, 0] for i in range(dataframe[k].size)],
            values = dataframe[k].values,
            dense_shape = [dataframe[k].size, 1])
                        for k in CATEGORICAL_COLUMNS}
    feature_columns = dict(continous_cols.items() + categorical_cols.items())
    label = tf.constant(dataframe[LABEL_COLUMN].values)
    return feature_columns, label

