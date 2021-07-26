# # import json
# import requests

name_list = []
home_list = []
cover_list =[]
vid_list =[]
# resp = requests.get('https://official-joke-api.appspot.com/jokes/programming/ten')


import requests

url = "https://simpleanime.p.rapidapi.com/anime/list/recent"

headers = {
    'x-rapidapi-key': "ed05f6faedmsha141554d24b6379p1a82d6jsnad1adf5dc460",
    'x-rapidapi-host': "simpleanime.p.rapidapi.com"
    }

resp = requests.request("GET", url, headers=headers)
data = resp.json()

# print(data['data'][12]['title'])

for i in range(0,30):
    x = data['data'][i]['title']
    y = data['data'][i]['cover']
    z = data['data'][i]['date']
    n = data['data'][i]['vid_id']
    name_list.append(x)
    home_list.append(y)
    cover_list.append(z)
    vid_list.append(n)





