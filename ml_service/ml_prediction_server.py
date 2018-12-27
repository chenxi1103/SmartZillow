import pyjsonrpc
import tensorflow as tf
from ml_common import *
SERVER_HOST = 'localhost'
SERVER_PORT = 5050

MODEL_DIR  = './model/'

linear_regressor = tf.contrib.learn.LinearRegressor(
	feature_columns=feature_columns,
	optimizer=tf.train.AdamOptimizer(learning_rate=1),
	model_dir=MODEL_DIR,
)
print "model loading..."

class RequestHandler(pyjsonrpc.HttpRequestHandler):
	@pyjsonrpc.rpcmethod
	def predict(self, zipcode, property_type, bedroom, bathroom, size):
		sample = pandas.DataFrame({
			'zipcode':zipcode,
			'property_type':property_type,
			'bedroom':bedroom,
			'bathroom':bathroom,
			'size':size,
			'list_price':0,
			}, index=[0])
		def input_fn_predict():
			return input_fn(sample)
		prediction = linear_regressor.predict_scores(input_fn=input_fn_predict, as_iterable=False)[0].item()
		print prediction
		return prediction


http_server = pyjsonrpc.ThreadingHttpServer(
	server_address = (SERVER_HOST, SERVER_PORT),
	RequestHandlerClass = RequestHandler
)

print "Staring prediction server...."
print "URL: %s:%s" % (str(SERVER_HOST), str(SERVER_PORT))

http_server.serve_forever()

