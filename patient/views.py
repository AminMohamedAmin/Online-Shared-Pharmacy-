from django.shortcuts import render
from doctor.models import Medicine
from django.db.models import Q
from cart.forms import CartAddProductForm
from .models import Question, Messages
from login.models import Actions
import json
# Create your views here.


def Home(request):
    me = Medicine.objects.all()
    medi = []
    for i in me:
        medi.append(i.medicine_code)
        medi.append(i.medicine_name)

    return render(request, 'userhome.html', {'medi': json.dumps(medi)})

def Search(request):
    me = Medicine.objects.all()
    medi = []
    for i in me:
        medi.append(i.medicine_code)
        medi.append(i.medicine_name)

    med = request.POST['med']
    m = Medicine.objects.filter(Q(medicine_code=med)|Q(medicine_name=med))
    cart_product_form = CartAddProductForm()
    neww = Actions()
    neww.action = 'User Search for'+' ' + med + ' ' + 'Medicine'
    neww.type = 'Medicine_Search'
    neww.save()
    context = {
        'm':m,
        'med':med,
        'cart_product_form':cart_product_form,
        'medi': json.dumps(medi)
    }
    return render(request, 'userhome.html', context)


def Ask(request):
    me = Medicine.objects.all()
    medi = []
    for i in me:
        medi.append(i.medicine_code)
        medi.append(i.medicine_name)

    ask = request.POST['ask']
    new = Question()
    if request.user.is_authenticated:
        new.user = request.user.username
    else:
        new.user = 'visitor'
    new.quest = ask
    new.save()
    n = new.id
    nu = new.user

    neww = Actions()
    neww.action = 'User ask a Medical Question'
    neww.type = 'Medical_Question'
    neww.save()
    return render(request, 'userhome.html', {'n':n, 'nu':nu, 'ask':ask, 'medi': json.dumps(medi)})

def CheckAsk(request):
    me = Medicine.objects.all()
    medi = []
    for i in me:
        medi.append(i.medicine_code)
        medi.append(i.medicine_name)

    check = request.POST['check']
    if Question.objects.filter(id=check).exists():
        ch = Question.objects.get(id=check)
        neww = Actions()
        neww.action = 'User check for a Medical Reply'
        neww.type = 'Medical_Reply'
        neww.save()
        return render(request, 'userhome.html', {'ch':ch, 'check':check, 'medi': json.dumps(medi)})
    else:
        tt = 'there is no question related to this id, add a question down'
        return render(request, 'userhome.html', {'tt':tt, 'medi': json.dumps(medi)})

def Contact(request):
    me = Medicine.objects.all()
    medi = []
    for i in me:
        medi.append(i.medicine_code)
        medi.append(i.medicine_name)

    name = request.POST['Ne']
    email = request.POST['El']
    message = request.POST['Me']
    new = Messages()
    new.name = name
    new.email = email
    new.message = message
    new.save()
    text = 'message sent successfully, we will send reply to your email soon'

    neww = Actions()
    neww.action = 'User send a specific message'
    neww.type = 'Contact'
    neww.save()
    return render(request, 'userhome.html', {'text':text, 'medi': json.dumps(medi)})