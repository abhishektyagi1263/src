from django.urls import path,include
from .views import *
urlpatterns = [
    path('', home , name='home'),
    path('accounts/login/', login_attempt , name='login_attempt'),
    path('register', register_attempt , name='register_attempt'),
    path('token', token_send, name='token_send'),
    path('success', success , name='success'),
    path('verify/<auth_token>' , verify , name="verify"),
    path('error' , error_page , name="error"),
    path('detailview',detailview, name="detailview"),
   

    # path('accounts/logout',logout,name="logout")

]