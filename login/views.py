from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from doctor.models import Medicine
from .models import Actions
from datetime import datetime
import json
# Create your views here.

def InLog(request):
    return render(request, 'login.html', {})

def DrInLog(request):
    u = request.POST['unamee']
    p = request.POST['psww']
    result = authenticate(username=u, password=p)
    if result is not None and User.objects.get(username=u).is_superuser == True:
        login(request,result)
        new = Actions()
        new.action = 'Doctor Login to Site'
        new.type = 'Doctor'
        new.save()
        return HttpResponseRedirect('doctor')
    elif result is not None and User.objects.get(username=u).is_superuser == False:
        text = 'Faild, username is a patient not a doctor'
        return render(request, 'login.html', {'text': text})
    elif User.objects.filter(username=u).exists() == True and User.objects.get(username=u).password == p and User.objects.get(username=u).is_superuser == False and User.objects.get(username=u).is_staff == True:
        date = datetime.now()
        ll = User.objects.get(username=u)
        ll.last_login = date
        ll.save()
        new = Actions()
        new.action = 'Doctor Assistant Login to Site'
        new.type = 'Doctor'
        new.save()
        return HttpResponseRedirect('doctor')
    else:
        text = 'Faild, username and password are wrong. Check and try again'
        return render(request, 'login.html',{'text':text})

def user_sign(request):
    if User.objects.filter(username=request.POST['uname']).exists():
        text = 'Faild, username existed'
        return render(request, 'login.html', {'text':text})
    else:
        em = 'amain@gmail.com'
        user = User.objects.create_user(request.POST['uname'], em , request.POST['psw'])
        user.first_name = ''
        user.last_name = ''
        user.save()
        text = 'Success, sign up'
        new = Actions()
        new.action = 'New User Found'
        new.type = 'User'
        new.save()
        return render(request, 'login.html',{'text':text})

def UserInLog(request):
    u = request.POST['uuname']
    p = request.POST['ppsw']
    result = authenticate(username=u, password=p)
    if result is not None and User.objects.get(username=u).is_staff == False:
        login(request,result)
        new = Actions()
        new.action = 'User Login to Site'
        new.type = 'User'
        new.save()
        return HttpResponseRedirect('patient')
    elif result is not None and User.objects.get(username=u).is_staff == True:
        text = 'Faild, username is a doctor not a patient'
        return render(request, 'login.html', {'text': text})
    else:
        text = 'Faild, username and password are wrong. Check and try again'
        return render(request, 'login.html',{'text':text})

def DrForget(request):
    f = request.POST['forget']
    p = request.POST['new']
    if User.objects.filter(email=f).exists():
        u = User.objects.get(email=f)
        u.set_password(p)
        u.save()
    text = 'new password saved'
    new = Actions()
    new.action = 'Dr reset Password'
    new.type = 'Doctor'
    new.save()
    return render(request, 'login.html', {'text': text})

def DrOutlog(request):
    logout(request)
    return HttpResponseRedirect('/')

def Visit(request):
    me = Medicine.objects.all()
    medi = []
    for i in me:
        medi.append(i.medicine_code)
        medi.append(i.medicine_name)

    new = Actions()
    new.action = 'New Visitor Found'
    new.type = 'Visitor'
    new.save()
    return render(request, 'userhome.html', {'medi': json.dumps(medi)})