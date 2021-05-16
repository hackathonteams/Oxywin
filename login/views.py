from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from .models import Hospital
from .models import Producer
from .models import Transporter
from .models import Order
from django.contrib import messages
from django.db.models import Q

# Create your views here.
def index(request):
    return render(request,'index.html')

def register(request):
    if request.method == 'POST':
        role=request.POST['role']
        username=request.POST['username']
        name=request.POST['name']
        add=request.POST['add']
        state=request.POST['state']
        pin=request.POST['pin']
        email=request.POST['email']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']

        if pass1 != pass2:
            messages.error(request,'Password not Matching...')
            #print('Password Not matching')
            return redirect('register')
        elif User.objects.filter(username=username).exists():
            messages.error(request,'Username Taken')
            #print('Username Taken')
            return redirect('register')
        elif User.objects.filter(email=email).exists():
            messages.error(request,'E-mail already linked with different account.')
            #print('E-mail already linked with different account.')
            return redirect('register')
        else:
            user = User.objects.create_user(username=username,password=pass1, email=email, first_name=name, last_name=role)
            user.save()
            if role=='hospital':
                us = Hospital(id = user.id,name=name,address=add,state=state,pincode=pin,email=email,storage=0,rate=0,available=0,hours=0)
                us.save()
            elif role=='producer':
                us = Producer(id = user.id,name=name,address=add,state=state,pincode=pin,email=email,storage=0,rate=0,available=0)
                us.save()
            else:
                us = Transporter(id = user.id,name=name,address=add,state=state,pincode=pin,email=email,avail_tanker=0,capacity=0,total_tanker=0)
                us.save()

            return redirect('login') 
    else:
        return render(request,'register.html')

def login(request):
    if request.method=='POST':
        username=request.POST['username']
        pass1=request.POST['pass']

        user = auth.authenticate(username=username,password=pass1)

        if user is not None:
            auth.login(request,user)
            return redirect('dashboard')
        else:
            messages.error(request, 'invalid credentials')
            return redirect('login')
    else:
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

def edit(request):
    if request.method=='POST':
        user=request.user
        storage=request.POST['storage']
        remain=request.POST['remain']
        rate=request.POST['rate']
        if user.last_name == 'hospital':
            h = Hospital.objects.filter(Q(email__icontains = user.email))
            for x in h:
                x.storage=storage
                x.available=remain
                x.rate=rate
                x.hours=int(remain)/int(rate)
                x.save()
        elif user.last_name == 'producer':
            h = Producer.objects.filter(Q(email__icontains=user.email))
            for x in h:
                x.storage=storage
                x.available=remain
                x.rate=rate
                x.hours=int(remain)/int(rate)
                x.save()
        else:
            h = Transporter.objects.filter(Q(email__icontains=user.email))
            for x in h:
                x.total_tanker = storage
                x.avail_tanker = remain
                x.capacity = rate
                x.save()
        return redirect('dashboard')
    else:
        return render(request,'update.html')

def dash(request):
    user=request.user
    if user.last_name == 'hospital':
        h = Hospital.objects.filter(Q(email__icontains=user.email))
    elif user.last_name == 'producer':
        h = Producer.objects.filter(Q(email__icontains=user.email))
    elif user.last_name == 'transporter':
        h = Transporter.objects.filter(Q(email__icontains=user.email))
    return render(request,'dash.html',{'h':h})

def hos_order(request):
    if request.method=='POST':
        qty = request.POST['quantity']
        hours = request.POST['hours']
        user = request.user
        h = Hospital.objects.filter(Q(email__icontains=user.email))
        for x in h:
            id = x.id
        o = Order(hospital_ID=int(id),vendor_ID=0,transporter_ID=0,quantity=qty,hours=hours,status=1,SOS=0)
        o.save()
        return redirect('dashboard')
    else:
        return render(request,'hos_order.html')

def avail_orders(request):
    orders = Order.objects.all()
    hs = Hospital.objects.all()
    vs = Producer.objects.all()
    return render(request,'avail_orders.html',{'orders':orders,'hs':hs,'vs':vs})

def vaccept(request):
    orderid = request.POST['order_id']
    o = Order.objects.filter(Q(id__icontains=orderid))
    for order in o:
        if order.id==int(orderid):
            order.vendor_ID=request.user.id
            order.status=2
            order.save()
    return redirect('avail_orders')

def taccept(request):
    mail = request.user.email
    t = Transporter.objects.filter(Q(email__icontains = mail))
    orderid = request.POST['order_id']
    o = Order.objects.filter(Q(id__icontains=orderid))
    for x in t:
        t_id = x.id
    for order in o:
        if order.id==int(orderid):
            order.transporter_ID=t_id
            order.status=3
            order.save()
    return redirect('avail_orders')

def pickup(request):
    oid = request.POST['order_id']
    user = request.user
    o = Order.objects.filter(Q(id__icontains=oid))
    for order in o:
        if order.id == int(oid):
            vs = Producer.objects.filter(Q(id__icontains=order.vendor_ID))
            for x in vs:
                if x.id == int(order.vendor_ID):
                    x.available = x.available-order.quantity
                    x.save()
                    order.status = 4
                    order.save()
    return redirect('myorders')

def drop(request):
    oid = request.POST['order_id']
    user = request.user
    o = Order.objects.filter(Q(id__icontains=oid))
    for order in o:
        if order.id == int(oid):
            vs = Hospital.objects.filter(Q(id__icontains=order.hospital_ID))
            for x in vs:
                if x.id == int(order.hospital_ID):
                    x.available = x.available+order.quantity
                    x.save()
                    order.status = 5
                    order.save()
    return redirect('myorders')

def sos(request):
    oid = request.POST['order_id']
    orders = Order.objects.filter(Q(id__icontains=oid))
    for order in orders:
        if order.id == int(oid):
            order.SOS = 1
            order.save()
    return redirect('myorders')

def myorders(request):
    user = request.user
    hs = Hospital.objects.all()
    vs = Producer.objects.all()
    ts = Transporter.objects.all()
    orders = Order.objects.all()
    return render(request,'myorders.html',{'hs':hs,'vs':vs,'ts':ts,'orders':orders})