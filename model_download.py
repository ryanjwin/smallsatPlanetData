import requests
import pathlib
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os

# get environment variables
load_dotenv()
PLANET_API_KEY = os.environ.get('PLANET_API_KEY')
#get download information
def get_download_result(order_id, orders_url='https://api.planet.com/compute/ops/orders/v2'):
    url = orders_url + '/' + order_id
    r = requests.get(url, auth=HTTPBasicAuth(PLANET_API_KEY, ''))
    return r.json()['_links']['results']

# download order as a zip file
def download_order(results):
    results_urls = [r['location'] for r in results]
    results_names = [r['name'] for r in results]
    print('{} items to download'.format(len(results_urls)))

    for url, name in zip(results_urls, results_names):
        path = pathlib.Path(os.path.join('data', name))
        
        if not path.exists():
            print('downloading {} to {}'.format(name, path))
            r = requests.get(url, allow_redirects=True)
            path.parent.mkdir(parents=True, exist_ok=True)
            open(path, 'wb').write(r.content)
        else:
            print('{} already exists, skipping {}'.format(path, name))