from django.contrib import admin
from celebda.models import MatchCondition, Promoter, Influencer, Account

# Register your models here.

admin.site.register(MatchCondition)
admin.site.register(Promoter)
admin.site.register(Influencer)
admin.site.register(Account)