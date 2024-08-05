
# Replace these with your actual Naver API client ID and client secret
CLIENT_ID = '###'
CLIENT_SECRET = '###'

import requests
def naver_geocode(lat: float, lon: float):
    url = "https://naveropenapi.apigw.ntruss.com/map-reversegeocode/v2/gc"
    
    headers = {
        "X-NCP-APIGW-API-KEY-ID": CLIENT_ID,
        "X-NCP-APIGW-API-KEY": CLIENT_SECRET
    }
    
    params = {
        "coords": f"{lon},{lat}",
        "output": "json",
        "orders": "legalcode,admcode,addr"
    }
    
    response = requests.get(url, headers=headers, params=params)
    addr_data = response.json()['results'][0]['region']
    # return addr_data
    print(addr_data)
    return ' '.join([addr_data[key]['name'] for key in ['area1', 'area2', 'area3']]).strip()
