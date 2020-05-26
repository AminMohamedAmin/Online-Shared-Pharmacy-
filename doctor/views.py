from django.shortcuts import render, HttpResponseRedirect, redirect
from .models import Department, Medicine
from patient.models import Question, Messages
from orders.models import order, OrderItem, OrderSent
from django.db.models import Q
from django.contrib.auth.models import User
from login.models import Actions
from datetime import date, datetime, timedelta
from .models import Delivery
import json
from django.db.models import Count


# Create your views here.

def DocHome(request):
    d = Department.objects.all()
    m = Medicine.objects.all()
    o = order.objects.all()
    q = Question.objects.all()
    day = datetime.now().day
    qq = Question.objects.filter(created__day=day)
    oo = order.objects.filter(created__day=day)
    uu = User.objects.filter(date_joined__day=day)
    today = date.today()
    a = Actions.objects.filter(day=today).order_by('-created')

    users_list = order.objects.values_list('first_name', 'last_name', 'street', 'address', 'country').annotate(truck_count=Count('first_name')).order_by('-truck_count')[:3]
    cities_list = order.objects.values_list('country').annotate(truck_count=Count('country')).order_by('-truck_count')
    last_quest = Question.objects.last()
    last_message = Messages.objects.last()

    today = datetime.now()
    yesterday = today - timedelta(days=1)

    user_yesterday = User.objects.filter(date_joined__lte=yesterday, is_staff=False)
    user_today = User.objects.filter(date_joined__lte=today, is_staff=False)

    visitor_yesterday = Actions.objects.filter(type='Visitor', created__lte=yesterday)
    visitor_today = Actions.objects.filter(type='Visitor', created__lte=today)

    order_yesterday = order.objects.filter(created__lte=yesterday)
    order_today = order.objects.filter(created__lte=today)

    context = {
        'd':d,
        'm':m,
        'o':o,
        'q':q,
        'qq':qq,
        'uu':uu,
        'oo':oo,
        'a':a,
        'today':today,
        'cities_list':cities_list,
        'users_list':users_list,
        'last_quest':last_quest,
        'last_message':last_message,
        'user_yesterday':user_yesterday,
        'user_today':user_today,
        'visitor_yesterday':visitor_yesterday,
        'visitor_today':visitor_today,
        'order_yesterday':order_yesterday,
        'order_today':order_today,
    }
    return render(request, 'dochome.html', context)

def Dep(request):
    d = Department.objects.all()
    depo = []
    for i in d:
        depo.append(i.department_code)
        depo.append(i.department_name)
    context = {
        'd': d,
        'depo': json.dumps(depo)
    }
    return render(request, 'dep.html', context)

def Med(request):
    m = Medicine.objects.all()
    d = Department.objects.all()
    medi = []
    for i in m:
        medi.append(i.medicine_code)
        medi.append(i.medicine_name)
    for ii in d:
        medi.append(ii.department_code)

    dep_list = Medicine.objects.values_list('department', flat=True).distinct()
    context = {
        'm':m,
        'd':d,
        'dep_list':dep_list,
        'medi': json.dumps(medi)
    }
    return render(request, 'medi.html', context)

def DepState(request, id):
    d = Department.objects.all()
    depo = []
    for i in d:
        depo.append(i.department_code)
        depo.append(i.department_name)
    depstste = Medicine.objects.filter(department_id=id)
    context = {
        'depstste':depstste,
        'd':d,
        'id': id,
        'depo': json.dumps(depo)
    }
    return render(request, 'dep.html', context)


def AllDepState(request):
    dp = Department.objects.all()
    depo = []
    for i in dp:
        depo.append(i.department_code)
        depo.append(i.department_name)
    d = []
    dc = []
    dn = []
    di = []
    st = []
    for item in dp:
        m_id = item.id
        depstste = Medicine.objects.filter(department_id=m_id)
        if depstste.count() < item.department_items:
            d.append(item.department_code)
    for i in d:
        dep = Department.objects.filter(department_code=i)
        for ii in dep:
            dc.append(ii.id)
            dn.append(ii.department_name)
            di.append(ii.department_items)
    for it in dc:
        state = Medicine.objects.filter(department_id=it)
        st.append(state.count())
    le = len(d)
    context = {
        'dp':dp,
        'd':d,
        'dc': dc,
        'dn': dn,
        'di': di,
        'st':st,
        'le':le,
        'depo': json.dumps(depo)
    }
    return render(request, 'alldep.html', context)

def DepSearch(request):
    try:
        d = Department.objects.all()
        depo = []
        for i in d:
            depo.append(i.department_code)
            depo.append(i.department_name)
        search = request.GET.get('search')
        data = d.filter(
            Q(department_code=search) |
            Q(department_name=search)
        )
        st = []
        for item in data:
            m_id = item.id
            depstste = Medicine.objects.filter(department_id=m_id)
            # if depstste.count() < item.department_items and code == item.department_code:
            #     st.append(item.department_items - depstste.count())
            # else:
            #     st.append('good')
        context = {
            'd':d,
            'data':data,
            'st':st,
            'depstste':depstste,
            'm_id':m_id,
            'depo': json.dumps(depo)
        }
        return render(request, 'depsearch.html', context)
    except:
        return render(request, 'depsearch.html', {})

def AllMedState(request):
    me = Medicine.objects.all()
    de = Department.objects.all()
    medi = []
    for i in me:
        medi.append(i.medicine_code)
        medi.append(i.medicine_name)
    for ii in de:
        medi.append(ii.department_code)

    m = Medicine.objects.filter(medicine_quantity__lt=10)
    mm = Medicine.objects.all()
    dep_list = m.values_list('department', flat=True).distinct()
    dep_listt = mm.values_list('department', flat=True).distinct()
    context = {
        'm':m,
        'dep_list':dep_list,
        'mm': mm,
        'dep_listt': dep_listt,
        'medi': json.dumps(medi)
    }
    return render(request, 'allmed.html', context)

def MedSearch(request):
    m = Medicine.objects.all()
    d = Department.objects.all()
    medi = []
    for i in m:
        medi.append(i.medicine_code)
        medi.append(i.medicine_name)
    for ii in d:
        medi.append(ii.department_code)

    search = request.GET.get('search')
    if d.filter(department_code=search).exists():
        ss = d.get(department_code=search).id
        data = m.filter(
            Q(department_id=ss)
        )
    else:
        data = m.filter(
            Q(medicine_code=search) |
            Q(medicine_name=search)
        )
    dep_list = data.values_list('department', flat=True).distinct()
    context = {
        'data':data,
        'm':m,
        'd':d,
        'dep_list':dep_list,
        'medi': json.dumps(medi)
    }
    return render(request, 'medsearch.html', context)


def Order(request):
    o = order.objects.all()
    oi = OrderItem.objects.all()
    os = OrderSent.objects.all()
    do = 'Dr'
    da = 'Dr Assistant'
    context = {
        'o':o,
        'oi': oi,
        'os':os,
        'do':do,
        'da':da,
    }
    return render(request, 'order.html', context)

def TodayOrders(request):
    day = datetime.now().date()
    o = order.objects.filter(date=day)
    oi = OrderItem.objects.all()
    os = OrderSent.objects.all()
    do = 'Dr'
    da = 'Dr Assistant'
    context = {
        'o': o,
        'oi': oi,
        'os': os,
        'do': do,
        'da': da,
    }
    return render(request, 'order.html', context)

def NotSentOrders(request):
    o = order.objects.filter(sent=False)
    oi = OrderItem.objects.all()
    os = OrderSent.objects.all()
    do = 'Dr'
    da = 'Dr Assistant'
    context = {
        'o': o,
        'oi': oi,
        'os': os,
        'do': do,
        'da': da,
    }
    return render(request, 'order.html', context)

def NotPaidOrders(request):
    o = order.objects.filter(sent=True, paid=False)
    oi = OrderItem.objects.all()
    os = OrderSent.objects.all()
    do = 'Dr'
    da = 'Dr Assistant'
    context = {
        'o': o,
        'oi': oi,
        'os': os,
        'do': do,
        'da': da,
    }
    return render(request, 'order.html', context)

def SearchOrders(request):
    order_idd = request.GET.get('order_idd')
    o = order.objects.filter(id=order_idd)
    oi = OrderItem.objects.all()
    os = OrderSent.objects.all()
    do = 'Dr'
    da = 'Dr Assistant'
    context = {
        'o': o,
        'oi': oi,
        'os': os,
        'do': do,
        'da': da,
    }
    return render(request, 'order.html', context)

def DliverManOrders(request):
    ord_deliver = request.POST['ord_deliver']
    o = order.objects.filter(sent=True)
    os = OrderSent.objects.filter(delivery_man=ord_deliver)
    oi = OrderItem.objects.all()

    dl = Delivery.objects.filter(code=ord_deliver)

    do = 'Dr'
    da = 'Dr Assistant'
    context = {
        'o': o,
        'oi': oi,
        'os': os,
        'do': do,
        'da': da,
        'dl':dl,
    }
    return render(request, 'orderdeliver.html', context)

def AskQuest(request):
    q = Question.objects.all().order_by('-created')
    do = 'Dr'
    da = 'Dr Assistant'
    return render(request, 'ask.html', {'q':q, 'do':do, 'da':da})

def AskQuestNotReply(request):
    q = Question.objects.filter(reply='').order_by('-created')
    do = 'Dr'
    da = 'Dr Assistant'
    return render(request, 'ask.html', {'q':q, 'do':do, 'da':da})

def Replying(request, id):
    repl = request.POST['repl']
    qu = request.POST['qu']
    us = request.POST['us']
    ad = request.POST['ad']
    new = Question.objects.get(id=id)
    new.reply = repl
    new.user = us
    new.quest = qu
    new.admin = ad
    new.save()
    q = Question.objects.all().order_by('-created')
    neww = Actions()
    neww.action = 'Admin reply to question ' + ' ' + str(id)
    neww.type = 'Medical_Reply'
    neww.save()
    return render(request, 'ask.html', {'q':q})

def Users(request):
    u = User.objects.filter(is_staff=False)
    ad = User.objects.filter(is_staff=True)
    dl = Delivery.objects.all()
    v = Actions.objects.filter(action='New Visitor Found')
    return render(request, 'users.html', {'u':u, 'ad':ad, 'v':v, 'dl':dl})

def Feeds(request):
    a = Actions.objects.all().order_by('-created')
    return render(request, 'feeds.html', {'a':a})

def AddDep(request):
    dep_code = request.POST['dep_code']
    dep_name = request.POST['dep_name']
    dep_items = request.POST['dep_items']
    new = Department()
    new.department_code = dep_code
    new.department_name = dep_name
    new.slug = dep_name
    new.department_items = dep_items
    new.save()
    d = Department.objects.all()
    depo = []
    for i in d:
        depo.append(i.department_code)
        depo.append(i.department_name)
    neww = Actions()
    neww.action = 'New Department' + ' ' + str(new.id) + ' ' + 'added'
    neww.type = 'Department'
    neww.save()
    return render(request, 'dep.html', {'d':d, 'depo': json.dumps(depo)})

def EditDep(request, id):
    dep_edit = Department.objects.get(id=id)
    return render(request, 'editdep.html', {'dep_edit':dep_edit})

def SaveEditDep(request, id):
    dep_code = request.POST['dep_code']
    dep_name = request.POST['dep_name']
    dep_items = request.POST['dep_items']
    new = Department.objects.get(id=id)
    new.department_code = dep_code
    new.department_name = dep_name
    new.slug = dep_name
    new.department_items = dep_items
    new.save()
    d = Department.objects.all()
    depo = []
    for i in d:
        depo.append(i.department_code)
        depo.append(i.department_name)
    neww = Actions()
    neww.action = 'Department' + ' ' + str(id) + ' ' + 'updated'
    neww.type = 'Department'
    neww.save()
    return render(request, 'dep.html', {'d': d, 'depo': json.dumps(depo)})

def DeleteDep(request, id):
    dep_delete = Department(id=id)
    dep_delete.delete()
    d = Department.objects.all()
    depo = []
    for i in d:
        depo.append(i.department_code)
        depo.append(i.department_name)
    neww = Actions()
    neww.action = 'Department' + ' ' + str(id) + ' ' + 'deleted'
    neww.type = 'Department'
    neww.save()
    return render(request, 'dep.html', {'d': d, 'depo': json.dumps(depo)})

def AddMed(request):
    dep_cod = request.POST['dep_cod']
    depcode = Department.objects.get(department_code=dep_cod).id
    med_code = request.POST['med_code']
    med_name = request.POST['med_name']
    med_quant = request.POST['med_quant']
    med_price = request.POST['med_price']
    med_desc = request.POST['med_desc']
    new = Medicine()
    new.department_id = depcode
    new.medicine_code = med_code
    new.medicine_name = med_name
    new.slug = med_name
    new.medicine_quantity = med_quant
    new.medicine_price = med_price
    new.medicine_desc = med_desc
    new.save()
    neww = Actions()
    neww.action = 'New Medicine' + ' ' + str(new.id) + ' ' + 'added'
    neww.type = 'Medicine'
    neww.save()
    return redirect('med')

def EditMed(request, id):
    med_edit = Medicine.objects.get(id=id)
    d = Department.objects.all()
    return render(request, 'editmed.html', {'med_edit':med_edit, 'd':d})

def SaveEditMed(request, id):
    dep_cod = request.POST['dep_code']
    depcode = Department.objects.get(department_code=dep_cod).id
    med_code = request.POST['med_code']
    med_name = request.POST['med_name']
    med_quant = request.POST['med_quant']
    med_price = request.POST['med_price']
    med_desc = request.POST['med_desc']
    new = Medicine.objects.get(id=id)
    new.department_id = depcode
    new.medicine_code = med_code
    new.medicine_name = med_name
    new.slug = med_name
    new.medicine_quantity = med_quant
    new.medicine_price = med_price
    new.medicine_desc = med_desc
    new.save()
    neww = Actions()
    neww.action = 'Medicine' + ' ' + str(new.id) + ' ' + 'updated'
    neww.type = 'Medicine'
    neww.save()
    return redirect('med')

def DeleteMed(request, id):
    med_delete = Medicine.objects.get(id=id)
    med_delete.delete()
    neww = Actions()
    neww.action = 'Medicine' + ' ' + str(id) + ' ' + 'deleted'
    neww.type = 'Medicine'
    neww.save()
    return redirect('med')

def AddAdmin(request):
    ad_name = request.POST['ad_name']
    ad_email = request.POST['ad_email']
    ad_pass = request.POST['ad_pass']
    ad = User()
    ad.username = ad_name
    ad.email = ad_email
    ad.password = ad_pass
    ad.first_name = ''
    ad.last_name = ''
    ad.is_staff = True
    ad.is_superuser = False
    ad.save()
    neww = Actions()
    neww.action = 'New Admin' + ' ' + str(ad.username) + ' ' + 'added'
    neww.type = 'Admin'
    neww.save()
    return redirect('user')

def DeleteAdmin(request, id):
    uu = User.objects.get(id=id).username
    admin_delete = User.objects.get(id=id)
    admin_delete.delete()
    neww = Actions()
    neww.action = 'Admin' + ' ' + str(uu) + ' ' + 'deleted'
    neww.type = 'Admin'
    neww.save()
    return redirect('user')

def AddDeliver(request):
    dl_name = request.POST['dl_name']
    dl_address = request.POST['dl_address']
    dl_nid = request.POST['dl_nid']
    dl_code = request.POST['dl_code']
    dl = Delivery()
    dl.name = dl_name
    dl.address = dl_address
    dl.NID = dl_nid
    dl.code = dl_code
    dl.save()
    neww = Actions()
    neww.action = 'New DeliveryMan' + ' ' + str(dl.name) + ' ' + 'added'
    neww.type = 'Delivery'
    neww.save()
    return redirect('user')

def DeleteDeliver(request, id):
    uu = Delivery.objects.get(id=id).name
    deliver_delete = Delivery.objects.get(id=id)
    deliver_delete.delete()
    neww = Actions()
    neww.action = 'DeliveryMan' + ' ' + str(uu) + ' ' + 'deleted'
    neww.type = 'Delivery'
    neww.save()
    return redirect('user')

def SendOrder(request):
    Order_ID = request.POST['Order_ID']
    Admin_Username = request.POST['Admin_Username']
    DeliveryMan_Code = request.POST['DeliveryMan_Code']
    if Delivery.objects.filter(code=DeliveryMan_Code).exists() == True:
        dliver = OrderSent()
        dliver.order_id = Order_ID
        dliver.admin_uname = Admin_Username
        dliver.delivery_man = DeliveryMan_Code
        dliver.save()
        ord = order.objects.get(id=Order_ID)
        ord.sent = True
        ord.save()
        neww = Actions()
        neww.action = 'Order' + ' ' + str(Order_ID) + ' ' + 'sent by' + ' ' + str(DeliveryMan_Code)
        neww.type = 'Order'
        neww.save()
        return redirect('orders')
    return redirect('orders')

def PaidOrder(request, id):
    p = order.objects.get(id=id)
    if p.sent == True:
        p.paid = True
        p.save()
        neww = Actions()
        neww.action = 'Order' + ' ' + str(id) + ' ' + 'paid'
        neww.type = 'Order'
        neww.save()
        return redirect('orders')
    return redirect('orders')

def Contacts(request):
    c = Messages.objects.all().order_by('created')
    return render(request, 'contacts.html', {'c':c})

def DeleteContact(request, id):
    c = Messages.objects.get(id=id)
    c.delete()
    neww = Actions()
    neww.action = 'Contact Message' + ' ' + str(id) + ' ' + 'deleted'
    neww.type = 'Contact'
    neww.save()
    return redirect('contact')
