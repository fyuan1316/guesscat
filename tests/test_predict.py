from __future__ import print_function
from server import *
import requests


def test_taxi_restful_predict():

    host = 'http://{}:{}/v1/models/chicago-taxi:predict'.format(
        '150.109.69.83', '30418')
    data = '{"signature_name":"predict", "instances": [{"fare": 12.85, "trip_start_hour": 11, "pickup_census_tract": "", "dropoff_census_tract": "17031320400", "company": "Taxi Affiliation Services", "trip_start_timestamp": 1393673400.0, "pickup_longitude": -87.679954768, "trip_start_month": 3, "trip_miles": 0.0, "dropoff_longitude": -87.621971652, "dropoff_community_area": "720", "pickup_community_area": "22", "payment_type": "Cash", "trip_seconds": 0.0, "trip_start_day": 7, "pickup_latitude": 41.920451512, "dropoff_latitude": 41.877406123}]}'
    headers = {'content-type': 'application/json'}

    r = requests.post(host, data, headers)
    print(r.json())


def test_cat_grpc_predict():

    file_path = '/Users/max/alauda/PycharmProjects/guesscat/static/photo/cat.jpg'
    print(classify(file_path))
