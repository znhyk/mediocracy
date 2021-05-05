from django.contrib import admin
from django.urls import path
from celebda import views

app_name = 'celebda'
urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.signup, name='signup'),
    path('login/', views.signin, name='signin'),
    path('<int:account_id>/', views.welcome_index, name='welcome_index'),
    path('<int:account_id>/myprofile/', views.my_profile, name='my_profile'),
    path('<int:account_id>/myprofile/<int:tango_id_self>/', views.subprofile_detail, name='subprofile_detail'),
    path('<int:account_id>/profilecreate/', views.profile_create, name='profile_create'),
    path('<int:account_id>/conditionform/', views.condition_form, name='condition_form'),
    path('<int:account_id>/wishmatchcondition/', views.wish_matchcondition, name='wish_matchcondition'),
    path('<int:account_id>/wishmatchcondition/<int:matchcondition_id>/', views.matchcondition_detail, name='matchcondition_detail'),
    path('<int:account_id>/<int:tango_id>/', views.partner_detail, name='partner_detail'),
    path('<int:account_id>/peekdirect/<int:direct_id>/', views.peek_direct, name='peek_direct'),
    path('<int:account_id>/peekfreak/<int:tango_id>/', views.peek_freak, name='peek_freak'),
    path('<int:account_id>/toggle/<int:tango_id>/', views.profile_like_toggle, name='toggle'),
    path('<int:account_id>/<int:matchcondition_id>/fork/', views.fork, name='fork'),
    path('<int:account_id>/<int:matchcondition_id>/promoterform/', views.promoter_form, name='form_p'),
    path('<int:account_id>/<int:matchcondition_id>/influencerform/', views.influencer_form, name='form_i'),
    path('<int:account_id>/<int:matchcondition_id>/resultspromoter/', views.promoter_results, name='results_p'),
    path('<int:account_id>/<int:matchcondition_id>/resultsinfluencer/', views.influencer_results, name='results_i'),
]
#정규표현식 중 \d가 정수 한자리를 의미하는가?