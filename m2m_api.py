import json 
import os 
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
def getScenes(lat,lon,cloudCover=15):
    key = auth()
    url = "https://m2m.cr.usgs.gov/api/api/json/stable"
    headers = {'X-Auth-Token': key['data']}   
    acquisitionFilter = {'end' : '2024-12-31','start' : '2024-01-01'}      
    # print(res)
    spatialFilter =  {'filterType' : "mbr",
                    'lowerLeft' : {'latitude' : (lat)-0.1 , 'longitude' :(lon)- 0.1},
                    'upperRight' : { 'latitude' : (lat)+0.1, 'longitude' : (lon)+0.1}}
    payload = {"datasetName": "landsat_ot_c2_l2",
        'sceneFilter' : {'spatialFilter' : spatialFilter,'acquisitionFilter' : acquisitionFilter,  "cloudCoverFilter": {
                "max": cloudCover,
                "min": 0
            }}}
    payload = json.dumps(payload)
    print("Searching scenes...\n\n")   

    scenes = json.loads(requests.post(url + "/scene-search", payload, headers=headers).text)
    
    if len(scenes['data']['results'])>0:
        # return [(i['displayId'],i['entityId']) for i in scenes['data']['results']]
        entityId = scenes['data']['results'][0]
        # # print(entityId)
        return scenes['data']['results']
        # os.mkdir("/raster/enti")
        # return entityId['entityId'],entityId['displayId'],DownloadScenes(entityId['entityId'])
    else:
        return dict(error="No Scenes Found")
def DownloadScenes(entityId):
    key = auth()
    url = "https://m2m.cr.usgs.gov/api/api/json/stable"
    headers = {'X-Auth-Token': key['data']}   
    payload = {'datasetName' : "landsat_ot_c2_l2", 'entityIds' : entityId}
        # Call the download to get the direct download urls
    res = json.loads(requests.post(url + "/download-options", json.dumps(payload), headers=headers).text)
    return res

# metaData = scenes['data']['results']
# payload = {'datasetName' : "landsat_ot_c2_l1", 'entityIds' : x}
# res = requests.post(url + "/download-options", json.dumps(payload), headers=headers).text          
# downloadData = json.loads(res)['data'][0]
# for i in scenes['data']['results']:
#     print(i['entityId'])
# label = datetime.datetime.now().strftime("%Y%m%d_%H%M%S") # Customized label using date time
# payload = {'downloads' : [{'entityId' : "L1_LC09_L1GT_090106_20211212_20230505_02_T2_MTL_TXT",
#                           'productId' : product['id']}],
#                              'label' : label}
# with open('data_krakatau.txt','a') as teks:
#     fileName = []
#     for x in scenes_name:
#         payload = {'datasetName' : "landsat_ot_c2_l1", 'entityIds' : x}
#         # Call the download to get the direct download urls
#         res = requests.post(url + "/download-options", json.dumps(payload), headers=headers).text          
#         downloadData = json.loads(res)['data'][0]
#         print(downloadData['id'])
#         for i in downloadData['secondaryDownloads']:
#             if 'B4' in i['displayId'] or 'B3' in i['displayId'] or 'B5' in i['displayId'] or 'B6' in i['displayId'] or 'B2' in i['displayId']:
#                 print(i['displayId'])
#                 fileName.append(i['displayId'])
#                 teks.write(i['displayId']+'\n')
#             # if 'B2' in i['displayId']:
#             #     print(i['displayId'])
#             #     fileName.append(i['displayId'])
#             #     teks.write(i['displayId']+'\n')
#     teks.close()
# getScenes()
