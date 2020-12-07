from django.shortcuts import render,redirect
from .form import *
from .models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.forms import modelformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import stripe
from django.shortcuts import get_object_or_404
from .serializer import *
from django.http import JsonResponse,HttpResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt

stripe.api_key ="sk_test_51HXU1lBChKoE2DJ5GxbZHlucEdwNdeixpDACweRrDsJYkGSQ3kWYSGCSsWJvCXxPiKgG6on3PblXiGCG1zIkJNa100Tun8BXx6"

# Create your views here.
@login_required(login_url='login')
def Home(request):

    form = AddCycleForm()
    if request.method == 'POST':
        form = AddCycleForm(request.POST, request.FILES)
        if form.is_valid():
            cycle = form.save(commit=False)
            cycle.save()
            images = request.FILES.getlist('images')
            for i in images:
                image = CycleImage.objects.create(cycle=cycle,side_image=i)
                image.save()
                messages.success(request,f'Item Added Successfully')
            return redirect('cycle_adminlist')

    return render(request,'peddal/home.html',{'form':form})



@login_required(login_url='login')
def ListCycle(request):
    cycle = Cycle.objects.all().order_by('-published_date')
    brand= Brand.objects.all()
    search = request.GET.get('searchbycyclename')
    searchbybrand = request.GET.get('brand')
    searchbycondition = request.GET.get('condition')
    if search:

        cycle = Cycle.objects.filter(name__icontains=search)

        return render(request, 'peddal/admin-detail.html', {'cycle': cycle,'brand':brand})
    if searchbybrand:

        search_brand = get_object_or_404(Brand,id=searchbybrand)
        cycle = search_brand.cycle_set.all()

        return render(request, 'peddal/admin-detail.html', {'cycle': cycle,'brand':brand})
    if searchbycondition:
        cycle = Cycle.objects.filter(condition=searchbycondition)
        return render(request, 'peddal/admin-detail.html', {'cycle': cycle, 'brand': brand})



    return render(request,'peddal/admin-detail.html',{'cycle':cycle,'brand':brand})

def CycleList(request):
    cycle = Cycle.objects.all()
    return render(request,'peddal/cycle_list.html',{'cycle':cycle})

def EditCycle(request,id):
    cycle= get_object_or_404(Cycle,id=id)
    form = AddCycleForm(instance=cycle)
    if request.method == 'POST':
        form = AddCycleForm(request.POST,request.FILES,instance=cycle)
        if form.is_valid():
            form.save()
            messages.success(request,f'Item Edited Successfully')
            return redirect('cycle_adminlist')

    return render(request,'peddal/admin-editcycle.html',{'form':form})

def DeleteCycle(request,id):
    cycle= Cycle.objects.get(id=id)
    cycle.delete()
    return redirect('cycle_adminlist')



@login_required(login_url='login')
def DetailCycle(request,id):
    cycle = Cycle.objects.get(id =id)
    cycle_image = cycle.cycleimage_set.all()
    return render(request,'peddal/cycle_detail.html',{'cycle':cycle,'image':cycle_image})


def Register(request):
    form = CreateUserForm()
    if request.method =='POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():

            form.save()
            user= form.cleaned_data.get('username')
            messages.success(request,'Account created for '+user)
            return redirect('login')


    return render(request, 'peddal/register.html', {'form': form})


def Login(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user.is_active:
            login(request,user=user)
            return redirect('home')
        else:
            return redirect('login')
    return render(request,'peddal/login-content.html',{})

def Logout(request):
    logout(request)
    return redirect('login')

def CustomerDetail(request):
    form = CustomerDetailForm()
    if request.method == 'POST':
        form = CustomerDetailForm(request.POST,request.FILES)
        if form.is_valid():
            user = request.user
            name= request.POST.get('name')
            address = request.POST.get('address')
            contact = request.POST.get('contact')
            profile_pic = request.FILES.get('profile_pic')

            customer = Customer.objects.create(user=user,name=name,address=address,contact=contact,profile_pic=profile_pic)
            customer.save()
    return render(request,'peddal/customerdetail.html',{'form':form})


@login_required(login_url='login')    
def RentalDetail(request,id):
    form = RentalForm()

    if request.method == 'POST':
        form = RentalForm(request.POST)
        if form.is_valid():
            user= request.user
            customer= user.customer
            cycle =Cycle.objects.get(id=id)
            if cycle.status == 'yes':
                rental_date = request.POST.get('rental_date')
                rental_time = request.POST.get('rental_time')
                return_date = request.POST.get('return_date')
                rental_status = request.POST.get('rental_status')
                if rental_status == 'on':

                   status = True

                else:
                  status = False

                rental = Rental(customer=customer,cycle=cycle,rental_date=rental_date,rental_time=rental_time,return_date=return_date,rental_status=status)
                rental.save()
                
            else:
                messages.error(request,'cycle Is already booked')
    return render(request,'peddal/rental.html',{'form':form})


def Payment(request):
    if request.method == 'POST':
        print('Data:', request.POST)
        customer = stripe.Customer.create(source = request.POST['stripeToken'])
        charge = stripe.Charge.create(
            customer =customer,
            amount=500,
            currency ='usd',
            description="Donation"
        )
    return render(request,'peddal/payment.html',{})





def CycleApi(request):
    if request.method == 'GET':
        cycle = Cycle.objects.all()
        ser = BookSerializer(cycle,many=True)
        return JsonResponse(ser.data, safe=False)
    if request.method == 'POST':
       data =  JSONParser().parse(request)
       print(data)
       ser=BookSerializer(data=data)
       if ser.is_valid():
           ser.save()
           return JsonResponse(ser.data)
       return JsonResponse(ser.errors,status=500)


def CycleObjectApi(request,id):
    cycle =Cycle.objects.get(id=id)
    if request.method == 'GET':
        
        ser=BookSerializer(cycle)
       
        return JsonResponse(ser.data)
    if request.method =='PUT':
        data= JSONParser().parse(request)
        ser = BookSerializer(cycle,data=data)
        if ser.is_valid():
            ser.save()

    if request.method == 'DELETE':
        cycle = Cycle.objects.get(id=id)
        cycle.delete()
        return HttpResponse(status=200)





CsrfCycleApi = csrf_exempt(CycleApi)
CsrfCycleObjectApi = csrf_exempt(CycleObjectApi)










