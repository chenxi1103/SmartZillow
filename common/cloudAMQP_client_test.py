from cloudAMQP_client import CloudAMQPClient

CLOUDAMQP_URL = 'amqp://ilrxmxve:Noyvd180oSB69hwc8dSgT_hEKJ1tkA3U@barnacle.rmq.cloudamqp.com/ilrxmxve'
QUEUE_NAME = 'dataFetcherTaskQueue'

# Initialize a client
client = CloudAMQPClient(CLOUDAMQP_URL, QUEUE_NAME)

# Send a message
client.sendDataFetcherTask({'name' : 'test message'})


# Receive a message
#client.getDataFetcherTask()
