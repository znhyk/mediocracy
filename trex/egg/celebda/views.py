from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views.generic import View
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib import auth
from celebda.models import MatchCondition, Promoter, Influencer, Account
from celebda.forms import MatchConditionForm, PromoterForm, InfluencerForm, UserForm, AccountForm, LoginForm
from django.db.models import Q
#데코레이터 @login required -> 보안에 필요.

# Create your views here.
#인덱스폼->매치컨디션DB채움->유저폼->I or P 결정(간단한)->각각에 맞는 결과 저장후 ->해당매치컨디션에 딸려있는 프로모터와 인플루언서를 교차하여 제출.
#index -> signin or signup -> welcome_index or profile_create -> welcome_index

def index(request):
    return render(request, 'celebda/index.html')

def welcome_index(request, account_id):#내가 Like한 유저, 새로가입한 유저를 갖고옴
    account_now = get_object_or_404(Account, pk=account_id)
    context = user_bringer(account_id)
    context['account_now'] = account_now
    return render(request, 'celebda/welcome_index.html', context)
    
def my_profile(request, account_id):
    account_now = get_object_or_404(Account, pk=account_id)
    context = subprofile_bringer(account_id)
    context_a = {'account_now': account_now}
    context.update(context_a)
    return render(request, 'celebda/my_profile.html', context)
    
def profile_create(request, account_id):#나중에 code cleaning (account_id=>register_id)할것!!!!!! 존나 헷갈림..
    if request.method == "POST":
        i_user_nick = request.POST['new_user_nick'] 
        i_introduce = request.POST['new_introduce']
        i_phone_num = request.POST['new_phone_num']
        i_is_promter = request.POST['iorp']
        i_photo = request.FILES.get('photo')
        new_account = Account(
            id=account_id,#Account와 User간의 pk-Syncro가 되어있지 않으면 welcome_index에서 404를 반환(Account는 3까지 생성됐는데 User pk=8, Account pk=8인 경우)
            user_id=account_id,
            user_nick=i_user_nick,
            phone_num=i_phone_num,
            introduce=i_introduce,
            is_promoter=i_is_promter,
            photo=i_photo,
            thum=i_photo,
        )
        new_account.save()
        return HttpResponseRedirect(reverse('celebda:welcome_index', args=(new_account.id,)))            
    else:
        return render(request, 'celebda/profile_create.html', {
            'account_id': account_id,
        })
    
def wish_matchcondition(request, account_id):#QRM 순서 어카운트->프/인->[매치콘]->인/프.
    pk_list=[]
    account_now = get_object_or_404(Account, pk=account_id)
    context = user_bringer(account_id)
    context_m = match_bringer(account_id)
    context.update(context_m)
    context['account_now'] = account_now
    return render(request, 'celebda/wish_match.html', context)
    
def matchcondition_detail(request, account_id, matchcondition_id):
    account_now = get_object_or_404(Account, pk=account_id)
    if account_now.is_promoter == 'P':
        context = promoter_results_maker(request, account_id, matchcondition_id)
    else:
        context = influencer_results_maker(request, account_id, matchcondition_id)
    return render(request, 'celebda/match_detail.html', context)

def subprofile_detail(request, account_id, tango_id_self):
    tango_id = tango_id_self
    account_now = get_object_or_404(Account, pk=account_id)
    if account_now.is_promoter == 'P':
        tango = get_object_or_404(Promoter, pk=tango_id)
    else:
        tango = get_object_or_404(Influencer, pk=tango_id)
    context = {
        'tango': tango,
        'account_now': account_now,
    }
    return render(request, 'celebda/partner_detail.html', context)

def partner_detail(request, account_id, tango_id):
    account_now = get_object_or_404(Account, pk=account_id)
    if account_now.is_promoter == 'P':
        tango = get_object_or_404(Influencer, pk=tango_id)
    else:
        tango = get_object_or_404(Promoter, pk=tango_id)
    context = {
        'tango': tango,
        'account_now': account_now,
    }
    return render(request, 'celebda/partner_detail.html', context)

"""def influencer_detail(request, account_id, influencer_id):
    account_now = get_object_or_404(Account, pk=account_id)
    tango = get_object_or_404(Influencer, pk=influencer_id)
    context = {
        'tango': tango,
        'account_now': account_now,
    }
    return render(request, 'celebda/influencer_detail.html', context)"""
    
def profile_like_toggle(request, account_id, tango_id):
    account_now = get_object_or_404(Account, pk=account_id)
    if account_now.is_promoter == 'P':
        influencer = get_object_or_404(Influencer, pk=tango_id)
        check_like_influencer = influencer.like.filter(id=account_id)
        if check_like_influencer.exists():
            influencer.like.remove(account_now)
            influencer.like_count -= 1
            influencer.save()
        else:
            influencer.like.add(account_now)
            influencer.like_count += 1
            influencer.save()
        return HttpResponseRedirect(reverse('celebda:partner_detail', kwargs={'account_id':account_now.id, 'tango_id':influencer.id}))
    else:
        promoter = get_object_or_404(Promoter, pk=tango_id)
        check_like_promoter = promoter.like.filter(id=account_id)
        if check_like_promoter.exists():
            promoter.like.remove(account_now)
            promoter.like_count -= 1
            promoter.save()
        else:
            promoter.like.add(account_now)
            promoter.like_count += 1
            promoter.save()        
        return HttpResponseRedirect(reverse('celebda:partner_detail', kwargs={'account_id':account_now.id, 'tango_id':promoter.id}))

"""def profile_like_toggle_i(request, account_id, influencer_id):
    influencer = get_object_or_404(Influencer, pk=influencer_id)
    account_now = get_object_or_404(Account, pk=account_id)
    check_like_influencer = influencer.like.filter(id=account_id)
    if check_like_influencer.exists():
        influencer.like.remove(account_now)
        influencer.like_count -= 1
        influencer.save()
    else:
        influencer.like.add(account_now)
        influencer.like_count += 1
        influencer.save()
    return HttpResponseRedirect(reverse('celebda:detail_i', args=(account_now.id, influencer.id,)))"""
    
def peek_freak(request, account_id, tango_id):#contract_detail.html 또는 다른 html에서 peek_num(상대 Influencer or Promoter의 id)을 받아온다.
    account_now = get_object_or_404(Account, pk=account_id)
    if account_now.is_promoter == 'P':
        tango = get_object_or_404(Influencer, pk=tango_id)
    else:
        tango = get_object_or_404(Promoter, pk=tango_id)
    peek_key = tango.account_id
    peeked_account = get_object_or_404(Account, pk=peek_key)
    context_a = subprofile_bringer(account_id=peek_key)
    context = {
        'peeked_account': peeked_account,
        'account_now': account_now,
    }
    context.update(context_a)
    return render(request, 'celebda/peek_freak.html', context)
    
def peek_direct(request, account_id, direct_id):
    account_now = get_object_or_404(Account, pk=account_id)
    peeked_account = get_object_or_404(Account, pk=direct_id)
    context_a = subprofile_bringer(account_id=direct_id)
    context = {
        'peeked_account': peeked_account,
        'account_now': account_now,
    }
    context.update(context_a)
    return render(request, 'celebda/peek_freak.html', context)

def condition_form(request, account_id):
    account_now = get_object_or_404(Account, pk=account_id)
    template_name = 'celebda/condition_form.html'
    if request.method == "POST":
        i_sex = request.POST['sex']
        i_age = request.POST['age']
        i_cost = request.POST['cost']
        i_field = request.POST['field']
        try:
            #Chaning, LAZY.         
            queryset = MatchCondition.objects.all()
            queryset = queryset.filter(sex=i_sex)
            queryset = queryset.filter(age=i_age)
            queryset = queryset.filter(cost=i_cost)
            queryset = queryset.get(field=i_field)
            matchcondition_id = queryset.id
            return HttpResponseRedirect(reverse('celebda:fork', kwargs={'account_id':account_now.id, 'matchcondition_id':matchcondition_id}))
                #pk로 넘겨주는것->이미 존재하는 매치콘디션의 id. 지연연산을 통해 리턴된 쿼리셋이 중복일 경우를 요주의할 것. 
        except:           
            new_condition = MatchCondition(sex=i_sex, age=i_age, cost=i_cost, field=i_field)
            new_condition.save()
            matchcondition_id = new_condition.id 
            return HttpResponseRedirect(reverse('celebda:fork', kwargs={'account_id':account_now.id, 'matchcondition_id':matchcondition_id}))#'%s/%s/fork/' %(account_num, pk)?
    else:
        return render(request, template_name, {
            'account_now': account_now,
        })

def fork(request, account_id, matchcondition_id): #공사중
    account_now = get_object_or_404(Account, pk=account_id)
    matchcondition = get_object_or_404(MatchCondition, pk=matchcondition_id)
    if account_now.is_promoter == 'P':
        return HttpResponseRedirect(reverse('celebda:form_p', kwargs={'account_id':account_now.id, 'matchcondition_id':matchcondition.id}))
    else:
        return HttpResponseRedirect(reverse('celebda:form_i', kwargs={'account_id':account_now.id, 'matchcondition_id':matchcondition.id}))
#위 HttpResponseRedirect에서 쓴 방법과 다르며, 무어가 맞는지 판단할 필요가 있습니다.

def promoter_form(request, account_id, matchcondition_id):
    account_now = get_object_or_404(Account, pk=account_id)
    matchcondition = get_object_or_404(MatchCondition, pk=matchcondition_id)
        
    if request.method == "POST":
        i_id_name = request.POST['new_id_name']
        i_introduce = request.POST['new_introduce']
        new_promoter = Promoter(account_id=account_now.id, matchcon_id=matchcondition.id, id_name=i_id_name, introduce=i_introduce)
        new_promoter.save()#외래키를 지정할 때는 그냥 'match'아닌 'match_id'로 정해주어야 함.
        return HttpResponseRedirect(reverse('celebda:results_p', kwargs={'account_id':account_now.id, 'matchcondition_id':matchcondition.id}))
    else:
        return render(request, 'celebda/form_p.html', {
            'matchcondition': matchcondition,
            'account_now': account_now,
        })

#https://stackoverflow.com/questions/27896272/how-to-create-forms-for-foreign-key-django
def influencer_form(request, account_id, matchcondition_id):
    account_now = get_object_or_404(Account, pk=account_id)
    matchcondition = get_object_or_404(MatchCondition, pk=matchcondition_id)
        
    if request.method == "POST":
        i_id_name = request.POST['new_id_name']
        i_introduce = request.POST['new_introduce']
        new_influencer = Influencer(account_id=account_now.id, matchcon_id=matchcondition.id, id_name=i_id_name, introduce=i_introduce)
        new_influencer.save()#외래키를 지정할 때는 그냥 'match'아닌 'match_id'로 정해주어야 함.
        return HttpResponseRedirect(reverse('celebda:results_i', kwargs={'account_id':account_now.id, 'matchcondition_id':matchcondition.id}))
    else:
        return render(request, 'celebda/form_i.html', {
            'matchcondition': matchcondition,
            'account_now': account_now,
        })
#https://brownbears.tistory.com/426 union -> 쿼리셋결과합치기. all=False는 중복금지.

def promoter_results(request, account_id, matchcondition_id):
    context = promoter_results_maker(request, account_id, matchcondition_id)
    return render(request, 'celebda/results_p.html', context)
    
def influencer_results(request, account_id, matchcondition_id):
    context = influencer_results_maker(request, account_id, matchcondition_id)
    return render(request, 'celebda/results_i.html', context)

def promoter_results_maker(request, account_id, matchcondition_id):
    pk_list = purifier(matchcondition_id)#pk_list를 받아온다. 용인가능한 조건들의 pk이며, 비어있을 수 있다.
    account_now = get_object_or_404(Account, pk=account_id)
    matchcondition = get_object_or_404(MatchCondition, pk=matchcondition_id)
    influencer_list = matchcondition.influencer_set.all()
    context = {
        'account_now': account_now,
        'matchcondition': matchcondition,
    }
    try:
        for num in pk_list:
            matchcondition = get_object_or_404(MatchCondition, pk=num)
            matset = matchcondition.influencer_set.all()
            influencer_list = influencer_list.union(matset, all=False)
    except:
        pass
    queryset = influencer_list
    try:
        for n in range(6):
            context['partner_%s' %(n+1)] = queryset[n]
    except:
        pass
    return context
        
def influencer_results_maker(request, account_id, matchcondition_id):
    pk_list = purifier(matchcondition_id)
    account_now = get_object_or_404(Account, pk=account_id)
    matchcondition = get_object_or_404(MatchCondition, pk=matchcondition_id)
    promoter_list = matchcondition.promoter_set.all()
    context = {
        'account_now': account_now,
        'matchcondition': matchcondition,
    }
    try:
        for num in pk_list:
            matchcondition = get_object_or_404(MatchCondition, pk=num)
            matset = matchcondition.promoter_set.all()
            promoter_list = promoter_list.union(matset, all=False)
    except:
        pass
    queryset = promoter_list
    try:
        for n in range(6):
            context['partner_%s' %(n+1)] = queryset[n]
    except:
        pass
    return context
    
def signup(request):
    if request.method == "POST":
        new_user = User.objects.create_user(
            username=request.POST["new_id"],
            password=request.POST["new_password"],
            email=request.POST["new_email"],
        )
        login(request, new_user)
        return HttpResponseRedirect(reverse('celebda:profile_create', kwargs={'account_id':new_user.id}))
    else:
        return render(request, 'celebda/signup.html')

#https://wayhome25.github.io/django/2017/03/01/django-99-my-first-project-2/

def signin(request):#함수이름이 login()과 겹치면 안됨.
    if request.method == "POST":
        username = request.POST["sign_id"]
        password = request.POST["sign_password"]
        user = authenticate(username = username, password = password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('celebda:welcome_index', args=(user.id,)))
        else:
            return HttpResponse('Login Failed, Try it Again!')
    else:
        return render(request, 'celebda/signin.html')

#View 보조함수
def purifier(matchcondition_id):
    pk_list = []
    fixed_list = []
    non_fixed_list = []
    matchcondition = get_object_or_404(MatchCondition, pk=matchcondition_id)
    i_sex = matchcondition.sex
    i_age = matchcondition.age
    i_cost = matchcondition.cost
    i_field = matchcondition.field
    queryset = MatchCondition.objects.all()
    value_dict = {
        'sex':i_sex,
        'age':i_age,
        'cost':i_cost,
        'field':i_field,
    }
    for key in value_dict:
        value = value_dict[key]
        if value == 'IR':
            non_fixed_list.append(key)
        else:
            fixed_list.append(key)
    for stone in fixed_list:
        if stone == 'sex':
            queryset = queryset.filter(sex=i_sex)
        elif stone == 'age':
            queryset = queryset.filter(age=i_age)
        elif stone == 'cost':
            queryset = queryset.filter(cost=i_cost)
        elif stone == 'field':
            queryset = queryset.filter(field=i_field)
        else:
            pass
    for water in non_fixed_list:
        if water == 'sex':
            queryset = queryset.exclude(sex='IR')
        elif water == 'age':
            queryset = queryset.exclude(age='IR')
        elif water == 'cost':
            queryset = queryset.exclude(cost='IR')
        elif water == 'field':
            queryset = queryset.exclude(field='IR')
        else:
            pass
    queryset_list = list(queryset)
    for n in range(len(queryset_list)):
        objval = queryset_list[n]
        pk_list.append(objval.id)
    return pk_list

def user_bringer(account_id):
    context = {}
    freshman_list = Account.objects.all().order_by('-join_date')[:3]
    account_now = get_object_or_404(Account, pk=account_id)
    if account_now.is_promoter == 'P':
        likedone_list = account_now.like_influencer.all().order_by('like_count')[:4]
    else:
        likedone_list = account_now.like_promoter.all().order_by('like_count')[:4]
    try:
        for n in range(3):
            context['freshman_%s' %(n+1)] = freshman_list[n]
    except:
        pass
    try:
        for n in range(4):
            context['likedone_%s' %(n+1)] = likedone_list[n]
    except:
        pass
    return context

def match_bringer(account_id):#QRM 순서 어카운트->프/인->[매치콘]->인/프.
    pk_list=[]
    context = {}
    account_now = get_object_or_404(Account, pk=account_id)
    if account_now.is_promoter == 'P':
        queryset = account_now.promoter_set.all()
    else:
        queryset = account_now.influencer_set.all()#account 주인의 p or i를 찾는다. 
    #queryset = queryset.filter(account_id=account_num)
    queryset = queryset.order_by('id')[:8]
    queryset_list = list(queryset)#이하; account 주인의 p or i들을 리스트에 담고, matchcon_id를 추출한다. 
    for n in range(len(queryset_list)):
        objval = queryset_list[n]
        pk_list.append(objval.matchcon_id)
    try:
        for n in range(8):
            context['match_%s' %(n+1)] = get_object_or_404(MatchCondition, pk=pk_list[n])
    except:
        pass
    return context
    
    """try:
        match_list = MatchCondition.objects.filter(id=pk_list[0])
        for num in pk_list:
            matchcondition = MatchCondition.objects.filter(id=num)
            match_list = match_list.union(matchcondition, all=False)
    except:
        pass"""
"""def partner_bringer(account_id, matchcondition_id):
    account_now = get_object_or_404(Account, pk=account_id)
    matchcondition = get_object_or_404(MatchCondition, pk=matchcondition_id)
    context = {
        'account_now': account_now,
        'matchcondition': matchcondition,
    }
    pk_list = purifier(matchcondition_id)
    try:
        for num in pk_list:
            if account_now.is_promoter == 'P':
                queryset = matchcondition.influencer_set.all()#.order_by('like_count')[:6]
                matchcondition = get_object_or_404(MatchCondition, pk=num)
                matset = matchcondition.influencer_set.all()
                queryset = queryset.union(matset, all=False)
            else:
                queryset = matchcondition.promoter_set.all()#.order_by('like_count')[:6]
                matchcondition = get_object_or_404(MatchCondition, pk=num)
                matset = matchcondition.promoter_set.all()
                queryset = queryset.union(matset, all=False)
    except:
        pass
    queryset = queryset.order_by('like_count')[:6]
    try:
        for n in range(6):
            context['partner_%s' %(n+1)] = queryset[n]
    except:
        pass
    return context"""

def subprofile_bringer(account_id):
    account_now = get_object_or_404(Account, pk=account_id)
    context = {}
    if account_now.is_promoter == 'P':
        queryset = account_now.promoter_set.all().order_by('-join_date')[:6]
    else:
        queryset = account_now.influencer_set.all().order_by('-join_date')[:6]
    try:
        for n in range(8):
            context['sub_%s' %(n+1)] = queryset[n]
    except:
        pass
    return context