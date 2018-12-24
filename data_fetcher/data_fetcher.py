import os
import sys
import time
import json
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
from cloudAMQP_client import CloudAMQPClient
import mongodb_client
import zillow_web_scraper_client

CLOUD_AMQP_URL = '''amqp://ilrxmxve:Noyvd180oSB69hwc8dSgT_hEKJ1tkA3U@barnacle.rmq.cloudamqp.com/ilrxmxve'''
DATA_FETCHER_QUEUE_NAME = 'dataFetcherTaskQueue'

PROPERTY_TABLE_NAME = 'property'

FETCH_SIMILAR_PROPERTIES = False

SECONDS_ONE_DAY = 3600 * 24
SECONDS_ONE_WEEK = SECONDS_ONE_DAY * 7

cloudAMQP_client = CloudAMQPClient(CLOUD_AMQP_URL, DATA_FETCHER_QUEUE_NAME)

def handle_message(msg):
    task = json.loads(msg)
    if (not isinstance(task,dict) or not 'zpid' in task or task['zpid'] is None):
        return
    
    # get the zpid
    zpid = task['zpid']

    # scrape the data based on zpid (unique)
    property_detail = zillow_web_scraper.get_property_by_zpid(zpid)

    # update the database (put the data into db)
    db = mongodb_client.getDB()
    db[PROPERTY_TABLE_NAME].replace_one({'zpid' : zpid}, property_detail, upsert=True)

    # 
    if FETCH_SIMILAR_PROPERTIES:
        # get its similar properties' zpids
        similar_zpids = zillow_web_scraper_client.get_similar_homes_for_sale_by_id(zpid)

        # generate tasks for similar zpids
        for zpid in similar_zpids:
            old = db[PROPERTY_TABLE_NAME].find_one({'zpid':zpid})
            
            # do not scrape the data that has been scraped in one week
            if (old is not None and time.time() - old['last_update'] < SECONDS_ONE_WEEK):
                continue
            cloudAMQP_client.sendDataFetcherTask({'zpid':zpid})

# main thread
while True:
    if cloudAMQP_client is not None:
        msg = cloudAMQP_client.getDataFetcherTask()
        if msg is not None:
            handle_message(msg)
        time.sleep(1)

