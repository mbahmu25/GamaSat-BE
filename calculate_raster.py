import json 
import requests

def auth():
    username = "gentiawan"
    pwd = "Gentiawan2505"
    url = "https://m2m.cr.usgs.gov/api/api/json/stable"
    data = {'username' : username, 'password' : pwd}
    json_data = json.dumps(data)
    response = requests.post(url+"/login", json_data)
    key = json.loads(response.text)
    return key
def getScenes():
    key = auth()
    url = "https://m2m.cr.usgs.gov/api/api/json/stable"
    headers = {'X-Auth-Token': key['data']}   
    acquisitionFilter = {'end' : '2023-12-31','start' : '2013-01-01'}      
    # print(res)
    spatialFilter =  {'filterType' : "mbr",
                    'lowerLeft' : {'latitude' : -5.98, 'longitude' :105.451111},
                    'upperRight' : { 'latitude' : -5.88416667, 'longitude' : 105.5102778}}
    payload = {"datasetName": "landsat_ot_c2_l2",
        'sceneFilter' : {'spatialFilter' : spatialFilter,'acquisitionFilter' : acquisitionFilter,  "cloudCoverFilter": {
                "max": 20,
                "min": 0
            }}}
    payload = json.dumps(payload)
    print("Searching scenes...\n\n")   

    scenes = json.loads(requests.post(url + "/scene-search", payload, headers=headers).text)
    return scenes
getScenes()