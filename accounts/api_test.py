import json
# import requests
name_list=[]
animetype=[]
episodes=[]
members=[]
smembers=[]
rating=[]
genre=[]
dates=[]
desc=[]
img_src=[]
english_name=[]
url=[]
genre1=[]
genre2=[]
genre3=[]
genre=[]
# animeid =[]
# import json
# with open('hum.txt') as f:
#     contents = f.read()
#     print(contents)
with open("D:/Binge watch/Create Account/src/accounts/js/m.json", "r") as read_file:
    # Convert JSON file to Python Types
    data = json.load(read_file)
  
#     # Pretty print JSON data
    pretty_json = json.dumps(data, indent=4)
    # print(data[1])
# data = f.read()
# obj = json.loads(data)
# data = json.load(f)
# print(data[1])
# resp = requests.get('https://official-joke-api.appspot.com/jokes/programming/ten')


# # ResponseObj.json()


print()
# for q in list1:
#    print(q[1:-1])  
for i in range(0,399):
    x = data[i]['name']
    y = data[i]['type']
    z = data[i]['episodes']
    a = data[i]['members']
    b = data[i]['score_members']
    c = data[i]['rating']
    d = data[i]['genre']
    e = data[i]['dates']
    f = data[i]['Description']
    g = data[i]['Image-SRC']
    h = data[i]['english_name']
    m = data[i]['url']
    
    conn=data[i]['genre'][1:-1]
    list1 = list(conn.split(", ")) 
    q=list1[0][1:-1]
    # print(list1)
    try:
        q1=list1[1][1:-1]
    except:
        q1=" "
    # print(list1[1])
    try:
        q2=list1[2][1:-1]
    except:
        q2=" "
    try:
        q3=list1[3][1:-1]
    except:
        q3=" "
    # q3=list1[3][1:-1]
    # print(type(i))
    # print(i)
    # j = data[i]['id']
    # animeid.append(j)
    name_list.append(x)
    animetype.append(y)
    episodes.append(z)
    members.append(a)
    smembers.append(b)
    rating.append(c)
    genre.append(d)
    dates.append(e)
    desc.append(f)
    img_src.append(g)
    english_name.append(h)
    url.append(m)
    genre.append(q)
    genre1.append(q1)
    genre2.append(q2)
    genre3.append(q3)
   





