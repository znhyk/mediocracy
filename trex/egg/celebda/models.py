from django.db import models
from django.contrib.auth.models import User
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

# Create your models here.
class MatchCondition(models.Model):
    SEX_CHOICES = (
        ('ML', 'Male'),
        ('FM', 'Female'),
        ('IR', 'Irelevance'),
    )
    sex = models.CharField(max_length=2, choices=SEX_CHOICES)
    AGE_CHOICES = (
        ('10S', '10s'),
        ('20S', '20s'),
        ('30S', '30s'),
        ('40S', '40s'),
        ('50S', '50s'),
        ('60S', '60s'),
        ('IR', 'Irelevance'),
    )
    age = models.CharField(max_length=3, choices=AGE_CHOICES)
    COST_CHOICES = (
        ('1MD', '1m'),
        ('10M', '10m'),
        ('1BU', '1b'),
        ('IR', 'Irelevance'),
    )   
    cost = models.CharField(max_length=3, choices=COST_CHOICES)
    FIELD_CHOICES = (
        ('F&B', 'Foods and Bevarage'),
        ('L&S', 'Leisure and Sports'),
        ('B&C', 'Beauty and Cosmetics'),
        ('IR', 'Irelevance'),
    )
    field = models.CharField(max_length=3, choices=FIELD_CHOICES)

def account_image_path(instance, filename):
    return f'account/{instance.is_promoter}/{instance.user_nick}/{instance.phone_num}.jpg'

def account_thum_path(instance, filename):
    return f'account/{instance.is_promoter}/{instance.user_nick}/{instance.phone_num}_thum.jpg'

class Account(models.Model):
    user_nick = models.CharField(max_length=30)
    introduce = models.TextField()
    phone_num = models.CharField(max_length=11)
    photo = ProcessedImageField(
                upload_to = account_image_path,
                processors = [ResizeToFill(300,350)], 
                format = 'JPEG', 
                options = {'quality': 90 }, 
        )
    thum = ProcessedImageField(
                upload_to = account_thum_path,
                processors = [ResizeToFill(90,90)],
                format = 'JPEG',
                options = {'quality': 90 },
        )
    PARTNER_CHOICES = (
        ('P', 'Promoter'),
        ('I', 'Influencer'),
    )
    is_promoter = models.CharField(max_length=1, choices=PARTNER_CHOICES)
    join_date = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user_nick

class Promoter(models.Model):
    id_name = models.CharField(max_length=30)
    introduce = models.CharField(max_length=200)
    join_date = models.DateTimeField(auto_now_add=True)
    matchcon = models.ForeignKey(MatchCondition, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    like = models.ManyToManyField(Account, blank=True, related_name='like_promoter')
    like_count = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.id_name

class Influencer(models.Model):
    id_name = models.CharField(max_length=30)
    introduce = models.CharField(max_length=200)
    join_date = models.DateTimeField(auto_now_add=True)
    matchcon = models.ForeignKey(MatchCondition, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    like = models.ManyToManyField(Account, blank=True, related_name='like_influencer')
    like_count = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.id_name

#https://infinitt.tistory.com/65?category=1072777

#https://dheldh77.tistory.com/entry/Django-%EC%9D%B4%EB%AF%B8%EC%A7%80-%EC%97%85%EB%A1%9C%EB%93%9C
#https://wayhome25.github.io/django/2017/05/10/media-file/ 
#https://tothefullest08.github.io/django/2019/06/04/Django17_image/