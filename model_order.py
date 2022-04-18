# import statements
from requests.auth import HTTPBasicAuth
import requests
import json
from dotenv import load_dotenv
import os
import pandas as pd

#load environment variables
load_dotenv()
PLANET_API_KEY = os.getenv('PLANET_API_KEY')

# specific region of interest
class Region:
    def __init__(self, name, region, dates, cloud_cover, item_type, asset_types, product_bundles):
        self.name = name
        # polygon json that contains coordinates of region of intrest
        self.region = region
        # locations that overlap region of interest
        self.location = {
            "type": "GeometryFilter",
            "field_name": "geometry",
            "config": region
        }
        # json that contains dates of interest
        self.dates = dates
        # json that has cloud cover threshol
        self.cloud_cover = cloud_cover
        # json that combines all previous filters
        self.filters = {
            "type": "AndFilter",
            "config": [self.location, dates, cloud_cover]
        }
        # item-type of images desired
        self.item_type = item_type
        # desired asset types
        self.asset_types = asset_types.split()
        # contain the bundles wanted, should correspond, same length, same index to asset_types
        self.product_bundles = product_bundles.split()
        # will contain ids of all images desired
        self.ids = {asset_type:[] for asset_type in self.asset_types}
        # save order object just in case
        self.order = None
        # will contain list of products
        self.products = []

def create_regions(path, ignore=[]):
    regions = []
    df = pd.read_csv(path)
    # create objects of regions
    for i in df.index:
        if df['Region Name'][i] not in ignore:
            regions.append(Region(df['Region Name'][i], json.loads(df['Polygon Coordinates'][i]), json.loads(df['Dates'][i]), json.loads(df['Cloud Coverage'][i]), df['Item Type'][i], df['Asset Type'][i], df['Product Bundle'][i]))
    return regions
    
def get_item_ids(region):
    # create a search with filters that we want for each region
    search = {
    "item_types":[region.item_type],
    "filter":region.filters
    }
    # post the request using our PLANET_API_KEY to authenticate
    search_result = \
        requests.post(
            'https://api.planet.com/data/v1/quick-search',
            auth=HTTPBasicAuth(PLANET_API_KEY, ''),
            json=search
        )
    # get the ids of the images that contain the asset_type we are looking for
    for feature in search_result.json()['features']:
        for asset_type in region.asset_types:
            if asset_type in feature['assets']:
                region.ids[asset_type].append(feature['id'])

# create products for order request
def create_products(region):
    for i, bundle in enumerate(region.product_bundles):
        region.products.append({
            "item_ids":region.ids[i],
            "item_type":region.item_type,
            "product_bundle":bundle
        })
def create_order(region):
    order = {
            'delivery': {'single_archive': True, 'archive_type': 'zip'},
            'name':region.name,
            'products':region.products,
            'notifications':{
               "email": True
            }
    }
    region.order = order

# place an order given an order request that contains the item ids
def place_order(region, auth=HTTPBasicAuth(PLANET_API_KEY, ''), headers = {'content-type': 'application/json'}, orders_url='https://api.planet.com/compute/ops/orders/v2'):
    request = region.order
    response = requests.post(orders_url, data=json.dumps(request), auth=auth, headers=headers)
    # show if response was successful
    print(response)
    order_id = response.json()['id']
    # print the id
    print(order_id)
    # return the order_id
    return order_id
