from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100 )
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class APIData(models.Model):
    # vid_id = models.CharField(max_length=50)
    # Home = models.CharField(max_length=50)
    # Cover = models.CharField(max_length=256, null= True)
    animeid = models.IntegerField(null=True)
    name = models.CharField(max_length=256)
    animetype = models.CharField(max_length=256,null=True)
    episodes = models.IntegerField(null=True)
    members = models.IntegerField(null=True)
    score_members= models.CharField(max_length=256,null=True)
    rating = models.DecimalField(max_digits=7, decimal_places=2,null=True)
    dates =models.CharField(null=True,max_length=256)
    description = models.TextField(null=True)
    img_src =  models.TextField(null=True)
    english_name = models.CharField(max_length=256,null=True)
    url= models.TextField(null=True)
    genre=models.CharField(max_length=256,null=True)
    genreb=models.CharField(max_length=256,null=True)
    genrec=models.CharField(max_length=256,null=True)
    genred=models.CharField(max_length=256,null=True)
    def __str__(self):
	    return self.name