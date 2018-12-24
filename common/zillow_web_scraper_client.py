import random
import re
import requests

from decimal import Decimal
from lxml import html
from re import sub
from urllib import pathname2url

URL = '''https://www.zillow.com'''
SEARCH_FOR_SALE_PATH = '''homes/for_sale'''
GET_PROPERTY_BY_ZPID_PATH = '''homes'''
GET_SIMILAR_HOMES_FOR_SALE_PATH = '''homedetails'''
IMAGE_URL_REGEX_PATTERN = '"z_listing_image_url":"([^"]+)",'
SIMILAR_HOMES_ZPID_REGEX_PATTERN ='\/(\d+)_zpid'

SEARCH_XPATH_FOR_ZPID = '''//div[@id='list-results']/div[@id='search-results']/ul[@class='photo-cards']/li/article/@id'''
GET_INFO_XPATH_FOR_STREET_ADDR = '''//header[@class='zsg-content-item']/h1[@class='zsg-h1']/div[@class='zsg-h1 hdp-home-header-st-addr']/text()'''
GET_INFO_XPATH_FOR_CITY_STATE_ZIP = '''//header[@class='zsg-content-item']/h1[@class='zsg-h1']/div[@class='zsg-h2']/text()'''
GET_INFO_XPATH_FOR_TYPE = '''//div[@class='fact-group zsg-lg-1-3 zsg-md-1-2'][1]/div[@class='zsg-media-bd']/div[@class='fact-value']/text()'''
GET_INFO_XPATH_FOR_BEDROOM = '''//header[@class='zsg-content-item']/h3[@class='edit-facts-light']/span[2]/text()'''
GET_INFO_XPATH_FOR_BATHROOM = '''//header[@class='zsg-content-item']/h3[@class='edit-facts-light']/span[4]/text()'''
GET_INFO_XPATH_FOR_SIZE = '''//header[@class='zsg-content-item']/h3[@class='edit-facts-light']/span[6]/text()'''
GET_INFO_XPATH_FOR_SALE = '''//div[@class='estimates']/div/div[@class='price']/span/text()'''
GET_INFO_XPATH_LIST_FOR_PRICE = '''//div[@class='estimates']/div/div[@class='zestimate']/div/text()[3]'''
GET_INFO_XPATH_DESCRIPTION = '''//div[@class=''][1]/text()'''
GET_INFO_XPATH_FOR_FACTS = '''//div[@class='fact-group zsg-lg-1-3 zsg-md-1-2']/div[@class='zsg-media-bd']/div/text()'''
GET_SIMILAR_HOMES_FOR_SALE_XPATH = '''//div[@class='zsg-photo-card-content zsg-aspect-ratio-content']/a/@href'''


GET_INFO_XPATH_FOR_LATITUDE = '''//div[@class='zsg-layout-top']/p/span/span[@itemprop='geo']/meta[@itemprop='latitude']/@content'''
GET_INFO_XPATH_FOR_LONGITUDE = '''//div[@class='zsg-layout-top']/p/span/span[@itemprop='geo']/meta[@itemprop='longitude']/@content'''
GET_INFO_XPATH_FOR_ADDITIONAL_FACTS = '''//div[@class='fact-group-container zsg-content-component z-moreless-content hide']/ul/li/text()'''

# Load user agents - pretend to be a real user!
USER_AGENTS_FILE = '../common/user_agents.txt'
USER_AGENTS = []

URL = '''http://www.zillow.com'''
GET_PROPERTY_BY_ZPID_PATH = '''homes'''
with open(USER_AGENTS_FILE, 'rb') as uaf:
    for ua in uaf.readlines():
        if ua:
            USER_AGENTS.append(ua.strip()[1:-1-1])
random.shuffle(USER_AGENTS)

def build_url(url,path):
    if url.endswith('/'):
        url = url[:-1]
    return '%s/%s' % (url,path)

def getHeaders():
    # randomly choose a user agent to pretend to be a real user
    ua = random.choice(USER_AGENTS) 
    headers = {
        "Connection" : "close",
        "User-Agent" : ua
    }
    return headers

def search_zillow(request_url, xpath):
    session_requests = requests.session()
    response = session_requests.get(request_url, headers=getHeaders())
    tree = html.fromstring(response.content)
    return tree.xpath(xpath)



''' Get property information by Zillow Property ID (zpid) '''
def get_property_by_zpid(zpid):
    request_url = '%s/%s_zpid' % (build_url(URL, GET_PROPERTY_BY_ZPID_PATH), str(zpid))
    print(request_url)
    session_requests = requests.session()
    response = session_requests.get(request_url)

    try:
        tree = html.fromstring(response.content)
    except Exception:
        return {}
    print(response.content)

    # Street address
    street_address = None
    try:
        street_address = tree.xpath(GET_INFO_XPATH_FOR_STREET_ADDR)[0].strip(', ')
    except Exception:
        pass

    # City, state and zipcode
    city_state_zip = None
    city = None
    state = None
    zipcode = None
    try:
        city_state_zip = tree.xpath(GET_INFO_XPATH_FOR_CITY_STATE_ZIP)[0]
        city = city_state_zip.split(',')[0].strip(', ')
        state = city_state_zip.split(',')[1].split(' ')[1].strip(', ')
        zipcode = city_state_zip.split(',')[1].split(' ')[2].strip(', ')
    except Exception:
        pass

    # Type: Condo, Town hourse, Single family etc.
    property_type = None
    try:
        property_type = tree.xpath(GET_INFO_XPATH_FOR_TYPE)[0]
    except Exception:
        pass

    # Bedroom
    bedroom = None
    try:
        bedroom = float(tree.xpath(GET_INFO_XPATH_FOR_BEDROOM)[0].split(' ')[0])
    except Exception:
        bedroom = 0

    # Bathroom (float since bathroom can be .5)
    bathroom = None
    try:
        bathroom = float(tree.xpath(GET_INFO_XPATH_FOR_BATHROOM)[0].split(' ')[0])
    except Exception:
        bathroom = 0

    # Square feet
    size = None
    try:
        size = int(tree.xpath(GET_INFO_XPATH_FOR_SIZE)[0].split(' ')[0].replace(',', ''))
    except Exception:
        size = 0

    # Is for sale
    for_sale_text = tree.xpath(GET_INFO_XPATH_FOR_SALE)
    r = re.compile('.+For Sale.+')
    is_for_sale = len(filter(r.match, for_sale_text)) > 0

    # Listed price
    list_price = None
    try:
        list_price_raw = tree.xpath(GET_INFO_XPATH_LIST_FOR_PRICE)
        if len(list_price_raw) > 0:
            list_price = float(list_price_raw[0].replace(',', '').strip(' $'))
    except Exception:
        pass

    # geo
    latitude = None
    longitude = None
    try:
        latitude = float(tree.xpath(GET_INFO_XPATH_FOR_LATITUDE)[0])
        longitude = float(tree.xpath(GET_INFO_XPATH_FOR_LONGITUDE)[0])
    except Exception:
        pass

    # Image
    image_url = None
    try:
        r = re.compile(IMAGE_URL_REGEX_PATTERN)
        result = r.search(response.content)
        image_url = result.group(1)
    except Exception:
        pass

    # Description
    description = None
    try:
        description = tree.xpath(GET_INFO_XPATH_DESCRIPTION)
    except Exception:
        pass

    # Basic facts
    facts = None
    try:
        facts = tree.xpath(GET_INFO_XPATH_FOR_FACTS)
    except Exception:
        pass

    # Additional facts
    additional_facts = None
    try:
        additional_facts = tree.xpath(GET_INFO_XPATH_FOR_ADDITIONAL_FACTS)
    except Exception:
        pass

    return {'zpid' : zpid,
            'street_address' : street_address,
            'city' : city,
            'state' : state,
            'zipcode' : zipcode,
            'property_type' : property_type,
            'bedroom' : bedroom,
            'bathroom' : bathroom,
            'size' : size,
            'latitude' : latitude,
            'longitude' : longitude,
            'is_for_sale' : is_for_sale,
            'list_price' : list_price,
            'image_url' : image_url,
            'description' : description,
            'facts' : facts,
            'additional_facts' : additional_facts}

''' Get similar homes for sale '''
def get_similar_homes_for_sale_by_id(zpid):
    pass
