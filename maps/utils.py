import numpy as np
import googlemaps
from itertools import product
import pandas as pd

def get_distance(result):
    return result[0]['legs'][0]['distance']['value']  # m

def get_miles(result):
    return np.round(get_distance(result) / 1609.34, 1)

def get_duration(result):
    return result[0]['legs'][0]['duration']['value']  # seconds

def get_minutes(result):
    return np.round(get_duration(result) / 60, 1)

class Gmaps(object):
    
    def __init__(self, key):
        self.client = googlemaps.Client(key=key)
        
    def run_queries(self, origin_addresses: list, destination_addresses: list, times:list, modes:list):
        results = []
        iterator = product(origin_addresses, modes, times, destination_addresses)
        for origin_address, mode, time, destination_address in iterator:
            result = self.query_gmaps(origin_address, destination_address, time, mode)
            results.append(result)
        results = pd.DataFrame(results)
        return results

    def query_gmaps(self, origin_address, destination_address, time, mode):
        result = {}
        arrival_time = time if mode != 'transit' else None
        query_result = self.client.directions(
            origin=origin_address, 
            destination=destination_address, 
            mode=mode,
            arrival_time=arrival_time,
            )
        result['origin_address'] =origin_address
        result['destination_address'] = destination_address
        result['mode'] = mode
        result['arrival_time'] = arrival_time.strftime('%H:%M') if arrival_time else np.nan
        try:
            result['dist_mi'] = get_miles(query_result)
            result['duration_min'] = get_minutes(query_result)
        except:
            pass
        return result