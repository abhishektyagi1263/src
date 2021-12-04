from accounts.models import Profile
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
import uuid
import pickle
import re
import pandas as pd
from random import randint
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.views.generic import View
from django.shortcuts import render
import requests
from .models import APIData
from . import api_test
from . import forms
# Create your views here.
# import eel
#importing eel


def data_preprocessing():

    #load the database
    anime_db = pd.read_csv('D:/Binge watch/Create Account/src/accounts/MAL_final_1.csv')
    anime_db.fillna('', inplace=True)
    
    
    return anime_db

# eel.init('web')
# eel.start('/')
# @eel.expose
# def fun_args(x):
#         print('hello %s' % x)



@login_required
def home(request):
   
    if request.GET and request.is_ajax:
        global dep 
        dep = request.GET.get('btn_text')
        print(type(dep))
        print("dep")
    else:
        # x_val = api_test.name_list
        
        # y_val = api_test.home_list
        # z_val = api_test.cover_list
        # n_val = api_test.vid_list
    # print(x_val)
    # print(n_val)
        # APIData.objects.all().delete()
        # for i in range(0,399):
        #     value = APIData(      
        #         # animeid = api_test.animeid[i],
        #         name = api_test.name_list[i],
        #         animetype=api_test.animetype[i],
        #         episodes=api_test.episodes[i],
        #         members=api_test.members[i],
        #         score_members=api_test.smembers[i],
        #         rating=api_test.rating[i],
        #         dates=api_test.dates[i],
        #         description=api_test.desc[i],
        #         img_src=api_test.img_src[i],
        #         english_name=api_test.english_name[i],
        #         genre = api_test.genre[i],
        #         genreb = api_test.genre1[i],
        #         genrec = api_test.genre2[i],
        #         genred = api_test.genre3[i],
        #         url=api_test.url[i],
               
        #         )
        #     value.save()
        data = APIData.objects.all()
   

        return render(request ,'home.html',{'data':data})


   

@login_required
def detailv(request,members): 
        print("strr")
        name = "naruto"
        strr= name.replace('%20',' ')
        print(strr+"hey")
        x=APIData.objects.get(members = members)
        return render(request,'detailv.html',
        {"data":x})

def similar_by_content(request,query):
    anime_db = data_preprocessing()
    # if request.method == 'POST':
    #     result = request.form
    # query = result['name']
    x=APIData.objects.get(name = query)
    

    #load the model file
    pkl_file = open('D:/Binge watch/Create Account/src/accounts/anime_indices.pkl', 'rb')
    indices = pickle.load(pkl_file)
    if query not in anime_db['name']:
        N = anime_db[anime_db['name'] == query].index[0]
        anime_list = []
        for n in indices[N][1:]:
            if query not in anime_db.loc[n]['name']:
                info = {
                    "name": anime_db.loc[n]['name'],
                    "english_name": anime_db.loc[n]['english_name'],
                    "rating": round(anime_db.loc[n]['rating'],2),
                    "genre": anime_db.loc[n]['genre'],
                    "type": anime_db.loc[n]['type'],
                    "MAL": anime_db.loc[n]['Image-SRC']
                    
                }    
                anime_list.append(info)
        print(anime_list[1])
        return render(request,"similar.html",{"data":x,"name":query,"topanime":anime_list})


@login_required
def gen(request,genre): 
       
        fil1=APIData.objects.filter(genre = genre)
        fil2=APIData.objects.filter(genreb = genre)
        fil3=APIData.objects.filter(genrec = genre)
        fil4=APIData.objects.filter(genred = genre)
        print(fil1)
        return render(request,'genre.html',
        {"fil1":fil1,"fil2":fil2,"fil3":fil3,"fil4":fil4,"typ":genre})


@login_required
def detailview(request):
    pq = "naruto"
    # nm = request.get['searchanime']
    searchform = forms.SearchForm()
    if request.method == 'POST':
        searchform = forms.SearchForm(request.POST)
        if searchform.is_valid():
            
            search_str = searchform.cleaned_data['search_anime']
            pq =  search_lower = search_str.lower()
            # pq = search_lower.replace(' ', '-')

   

    url = "https://jikan1.p.rapidapi.com/search/anime"

    querystring = {"q":pq}

    headers = {
        'x-rapidapi-host': "jikan1.p.rapidapi.com",
        'x-rapidapi-key': "cea1f021f9msh214c83f714f9882p1d15ebjsn23bbce7cadf2"
        }


       
    resp = requests.request("GET", url, headers=headers,params=querystring)
    data = resp.json()
    title = (data['results'][0]['title'])
    # stream = (data['data'][0]['stream'])
    # download = (data['data'][0]['download'])
    description = (data['results'][0]['synopsis'])
    cover = (data['results'][0]['image_url'])
    episode = (data['results'][0]['episodes'])
    typ = (data['results'][0]['score'])


    return render(request,'detailview.html',{
        'title':title,
        # 'stream':stream,
        # 'download':download,
        'description':description,
        'cover':cover,
        'episode':episode,
        'typ':typ,
        'searchform':searchform,
    })


def login_attempt(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username = username).first()
        if user_obj is None:
            messages.success(request, 'User not found.')
            return redirect('/accounts/login')
        
        
        profile_obj = Profile.objects.filter(user = user_obj ).first()

        if not profile_obj.is_verified:
            messages.success(request, 'Profile is not verified check your mail.')
            return redirect('/accounts/login')

        user = authenticate(username = username , password = password)
        if user is None:
            messages.success(request, 'Wrong password.')
            return redirect('/accounts/login')
        
        login(request , user)
        return redirect('/')

    return render(request , 'login.html')

def register_attempt(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(password)

        try:
            if User.objects.filter(username = username).first():
                messages.success(request, 'Username is taken.')
                return redirect('/register')

            if User.objects.filter(email = email).first():
                messages.success(request, 'Email is taken.')
                return redirect('/register')
            
            user_obj = User(username = username , email = email)
            user_obj.set_password(password)
            user_obj.save()
            auth_token = str(uuid.uuid4())
            profile_obj = Profile.objects.create(user = user_obj , auth_token = auth_token)
            profile_obj.save()
            send_mail_after_registration(email , auth_token)
            return redirect('/token')

        except Exception as e:
            print(e)


    return render(request , 'register.html')

def success(request):
    return render(request , 'success.html')


def token_send(request):
    return render(request , 'token_send.html')



def verify(request , auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token = auth_token).first()
    

        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified.')
                return redirect('/accounts/login')
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified.')
            return redirect('/accounts/login')
        else:
            return redirect('/error')
    except Exception as e:
        print(e)
        return redirect('/')

def error_page(request):
    return  render(request , 'error.html')








def send_mail_after_registration(email , token):
    subject = 'Your accounts need to be verified'
    message = f'Click on the link http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list )
    