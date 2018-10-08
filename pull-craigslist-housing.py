#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  2 17:45:53 2018

@author: vijayswamy
"""
import sys
from craigslist import CraigslistHousing
from math import radians, cos, sin, asin, sqrt
import pandas as pd
import csv
import numpy as np
import json
import pprint
import requests
import sys
import urllib

from urllib.error import HTTPError
from urllib.parse import quote
from urllib.parse import urlencode

API_KEY= '3nU3phN37fdNEA15I_fXlqa_E_zGaHQlaKho1jMgpKWxShPokBFLiSSHes_GTPYMr93WFF-hpFvVThpoFkSTHBKXUxrSADaHBqeePHflHk-fRWlUa-NleO-pxOWoW3Yx'
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.


# Defaults for our simple example.
DEFAULT_TERM = 'dinner'
DEFAULT_LOCATION = 'San Francisco, CA'
SEARCH_LIMIT = 3

app_id = 'oZHdFiJCLnokObkQ0RPJpw'
app_secret = API_KEY

def request(host, path, api_key, url_params=None):
    """Given your API_KEY, send a GET request to the API.
    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        API_KEY (str): Your API Key.
        url_params (dict): An optional set of query parameters in the request.
    Returns:
        dict: The JSON response from the request.
    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % api_key,
    }

    print(u'Querying {0} ...'.format(url))

    response = requests.request('GET', url, headers=headers, params=url_params)

    return response.json()

def search(api_key, category, latitude, longitude):
    """Query the Search API by a search term and location.
    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.
    Returns:
        dict: The JSON response from the request.
    """

    url_params = {
        'latitude': latitude,
        'longitude': longitude,
        'limit': SEARCH_LIMIT,
        'categories': category,
        'radius': 800,
        'price':[1,2]
    }
    return request(API_HOST, SEARCH_PATH, api_key, url_params=url_params)

def get_business(api_key, business_id):
    """Query the Business API by a business ID.
    Args:
        business_id (str): The ID of the business to query.
    Returns:
        dict: The JSON response from the request.
    """
    business_path = BUSINESS_PATH + business_id

    return request(API_HOST, business_path, api_key)

def query_api(term, location):
    """Queries the API by the input values from the user.
    Args:
        term (str): The search term to query.
        location (str): The location of the business to query.
    """
    response = search(API_KEY, term, location)

    businesses = response.get('businesses')

    if not businesses:
        print(u'No businesses for {0} in {1} found.'.format(term, location))
        return

    business_id = businesses[0]['id']

    print(u'{0} businesses found, querying business info ' \
        'for the top result "{1}" ...'.format(
            len(businesses), business_id))
    response = get_business(API_KEY, business_id)

    print(u'Result for business "{0}" found:'.format(business_id))
    pprint.pprint(response, indent=2)

cl = CraigslistHousing(site='newyork', area = 'manh', category='apa',
                         filters={'max_price': 2000, 'min_price': 1000})

results = cl.get_results(sort_by='newest', geotagged=True, limit=1000)
results = [result for result in results]

express_trains = {
    "72nd Street":(40.76871175277928,-73.95845890045166),
    "96th Street":(40.794220933640126,-73.97214889526367),
    "Rockefeller Center":(40.7586678722452,-73.98133277893066),
    "W 4th St":(40.7342315,-73.99880200000001),
    "125th St": (40.811568076586966,-73.95206451416016),
    "Canal St":(40.7182002,-73.99357359999999),
    "Grand St":(40.7182002,-73.99357359999999),
    "34th St":(40.750568,-73.99351899999999),
    "14th St":(40.7355816,-73.99219579999999),
    "Times Square": (40.7560445,-73.98778329999999),
    "Chambers Street": (40.76871175277928,-73.95845890045166),
    "57th Street": (37.790588199999995,-122.40038539999998)
}

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

geocode = [result["geotag"] for result in results]

areas = []
for result in results:
    if result["area"] != None:
        areas.append(result["area"])
    else:
        areas.append(242)

bedrooms = []
for result in results:
    if result["bedrooms"] != None:
        bedrooms.append(result["bedrooms"])
    else:
        bedrooms.append(0)

latitudes = []
longitudes = []
for geo in geocode:
    if geo != None:
        latitudes.append(geo[0])
        longitudes.append(geo[1])
    else:
        latitudes.append(0)
        longitudes.append(0)

near_train_results = []
near_pizza = []
near_bagels = []
near_convenience_store = []
near_cocktail_bars = []
near_food_trucks = []

for lat, long in zip(latitudes, longitudes):
    near_train = False
    for express_train in express_trains:
        if haversine(long, lat, express_trains[express_train][1], express_trains[express_train][0]) < 1:
            near_train = True
    if near_train == True:
        near_train_results.append(1)
    else:
        near_train_results.append(0)
    near_pizza.append(len(search(API_KEY, "pizza", lat, long)))
    near_bagels.append(len(search(API_KEY, "bagels", lat, long)))
    near_convenience_store.append(len(search(API_KEY, "convenience", lat, long)))
    near_cocktail_bars.append(len(search(API_KEY, "cocktailbars", lat, long)))
    near_food_trucks.append(len(search(API_KEY, "foodtrucks", lat, long)))

df["Latitude"] = latitudes
df["Longitude"] = longitudes
df["area"] = areas
df["bedrooms"] = bedrooms
df["Near_Express_Train"] = near_train_results
df["near_pizza"] = near_pizza
df["near_bagels"] = near_bagels
df["near_convenience_store"] = near_convenience_store
df["near_cocktail_bars"] = near_cocktail_bars
df["near_food_trucks"] = near_food_trucks
df["price"] = df["price"].apply(lambda x: x.replace('$','')).apply(lambda x: x.replace(',','')).astype(float)
df["area"] = df["area"].astype(str)
df["Interested"] = np.where((df["price"] > 1000) & (df["price"] < 2000) & (df["Near_Express_Train"] == 1),1,0)
df["area"] = df["area"].apply(lambda x: x.replace('ft2','')).astype(float)

with open('housing.csv', 'a') as f:
    df.to_csv(f, header=False)
