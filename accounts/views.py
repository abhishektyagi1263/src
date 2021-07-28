from accounts.models import Profile
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
import uuid
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

# eel.init('web')
# eel.start('/')
# @eel.expose
# def fun_args(x):
#         print('hello %s' % x)
text = 'myname'

@login_required
def home(request):
   
    if request.GET and request.is_ajax:
        text = request.GET.get('btn_text')
      
        url = "https://simpleanime.p.rapidapi.com/anime/info/videos/"+text

        headers = {
        'x-rapidapi-key': "ed05f6faedmsha141554d24b6379p1a82d6jsnad1adf5dc460",
        'x-rapidapi-host': "simpleanime.p.rapidapi.com"
        }
        
        resp = requests.request("GET", url, headers=headers)
        data = resp.json()
        title = (data['data'][0]['title'])
        stream = (data['data'][0]['stream'])
        download = (data['data'][0]['download'])
        description = (data['data'][0]['description'])
        cover = (data['episode'][0]['cover'])
        episode = (data['episode'][0]['episode'])
        typ = (data['episode'][0]['type'])
        print(url)

        return render(request,'detailv.html',{
            'title':title,
            'stream':stream,
            'download':download,
            'description':description,
            'cover':cover,
            'episode':episode,
            'typ':typ,
        
        })
    else:
        x_val = api_test.name_list
        y_val = api_test.home_list
        z_val = api_test.cover_list
        n_val = api_test.vid_list
    # print(x_val)
    # print(n_val)
        APIData.objects.all().delete()
        for i in range(0,30):
            value = APIData(
                name = x_val[i],
                Home = y_val[i],
                Cover =z_val[i],
                vid_id = n_val[i],
                )
            value.save()
        data = APIData.objects.all()
   

    return render(request ,'home.html',{'data':data})


   



@login_required
def detailview(request):
    pq = "mahou-no-star-magical-emi-episode-32"
    # nm = request.get['searchanime']
    searchform = forms.SearchForm()
    if request.method == 'POST':
        searchform = forms.SearchForm(request.POST)
        if searchform.is_valid():
            
            pq = searchform.cleaned_data['search_anime']

   
    
    url = "https://simpleanime.p.rapidapi.com/anime/info/videos/"+pq

    headers = {
        'x-rapidapi-key': "ed05f6faedmsha141554d24b6379p1a82d6jsnad1adf5dc460",
        'x-rapidapi-host': "simpleanime.p.rapidapi.com"
    }
    resp = requests.request("GET", url, headers=headers)
    data = resp.json()
    title = (data['data'][0]['title'])
    stream = (data['data'][0]['stream'])
    download = (data['data'][0]['download'])
    description = (data['data'][0]['description'])
    cover = (data['episode'][0]['cover'])
    episode = (data['episode'][0]['episode'])
    typ = (data['episode'][0]['type'])


    return render(request,'detailview.html',{
        'title':title,
        'stream':stream,
        'download':download,
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
    