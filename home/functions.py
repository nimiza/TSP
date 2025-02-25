import requests, os, platform, pandas as pn
from .api_keys import distance_api_key, coor_to_api_key







def neshan_distance_matrix(string):
    Api_Key = distance_api_key
    url = 'https://api.neshan.org/v1/distance-matrix'

    origins = string
    destinations = string


    headers = {
        'Api-Key': Api_Key
    }

    params = {
        'origins': origins,
        'destinations': destinations,
        'type': 'car',  # Type of travel: car, motor, foot
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()
        print(data)
        distance_matrix = []
        for row in data['rows']:
            distances = []
            for element in row['elements']:
                if element['status'] == 'Ok':
                    distances.append(element['distance']['value'])  # Use 'value' for meters
                else:
                    distances.append('N/A')  # Handle invalid or unreachable destinations
            distance_matrix.append(distances)
        print(distance_matrix)
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

    return distance_matrix


def neshan_cor_addr(lat, lon):
    Api_Key = coor_to_api_key
    url = 'https://api.neshan.org/v5/reverse'



    headers = {
        'Api-Key': Api_Key
    }

    params = {
        'lat': lat,
        'lng': lon,
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()

    else:
        print(f"Error: {response.status_code}")
        print(response.text)

    return(data['formatted_address'])


def ping(hostname='google.com'):
    param = '-n' if platform.system().lower()=='windows' else '-c'
    response = os.system(f"ping {param} 1 {hostname}")
    print(response)
    if response == 0:
        print(f"{hostname} is up!")
    else:
        print(f"{hostname} is down!")

    return response