from django.forms import ModelForm
from django import forms
from celebda.models import MatchCondition, Promoter, Influencer, Account
from django.contrib.auth.models import User

class MatchConditionForm(forms.ModelForm):
    class Meta:
        model = MatchCondition
        fields = ['sex', 'age', 'cost', 'field']

class PromoterForm(forms.ModelForm):
    class Meta:
        model = Promoter
        fields = ['id_name', 'introduce']
        
class InfluencerForm(forms.ModelForm):
    class Meta:
        model = Influencer
        fields = ['id_name', 'introduce']
        
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        
class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['user_nick', 'introduce', 'phone_num', 'is_promoter']