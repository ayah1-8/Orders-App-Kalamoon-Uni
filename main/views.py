from webbrowser import get
from wsgiref.util import request_uri
from django.forms.models import InlineForeignKeyField
from django.http import HttpResponseRedirect, request, response
from django.shortcuts import render, redirect,get_object_or_404
from django.http.response import HttpResponse, HttpResponseNotAllowed
from .decorators import *
from django.forms import fields, formsets, inlineformset_factory
from .models import *
from .forms import *
from .decorators import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages                              ##for flash messages
from django.contrib.auth.decorators import login_required        #####for restricting pages to logged users
from django.views.generic.list import ListView
import datetime
import xlwt
from copy import deepcopy


from django.http import JsonResponse
from django.template.loader import render_to_string

from oms_app.urls import *

def GetDevicecYear():
     currentDateTime = datetime.datetime.now()
     date = currentDateTime.date()
     return date.year

def GetDeviceDate():
     currentDateTime = datetime.datetime.now()
     date = currentDateTime.date()
     return date
# Create your views here.


################################################################################################################
##Login Page
@unauthenticated_user
def loginPage(request):
     if request.user.is_authenticated:
          if request.user.get_username() == 'Vice-President':
               return redirect('adminhome')
          else:
               return redirect('main:userhome')     
     else:
          if request.method == 'POST':
               username = request.POST.get('username')
               password = request.POST.get('password')
               user = authenticate(request, username=username, password = password)

               if user is not None:
                    login(request, user)
                    request.session['current_djangouser_id'] = user.id     #####each time the users sends a form it saves th annual id into this session
                    if request.user.get_username() == 'Vice-President':
                         return redirect('adminhome')
                    else:
                         return redirect('main:userhome') 

               else:
                    messages.info(request, 'Username OR password is incorrect')


          return render(request,'main/pages/login.html')


################################################################################################################
##LogOut View
@login_required(login_url='mainlogin')
def logoutUser(request):
     logout(request)  ########the logout flushes alllll sessions but after special authentication i need to add and flush them manually :())))
     # try:
     # except KeyError:
     #      pass
     return redirect('mainlogin') 

################################################################################################################
@login_required(login_url='mainlogin')
@allowed_users(allowed_roles=['Normal-Users'])
def HomeUser(request):

     currentdjangouser_S = request.session['current_djangouser_id']
     a = User.objects.get(user = currentdjangouser_S)

     year = GetDevicecYear()
     annualneedex = None
     AN = AnnualNeed.objects.filter(user = a).latest('YearDate')
     x = str(AN.yearofdoc())
     y = str(year)
     if (x == y):
          annualneedex = AN

     else:
          annualneed = AnnualNeed(YearDate = GetDeviceDate(), RequestingParty = a.RequestingParty, user =a)
          annualneed.save()
          annualneedex = annualneed
     an_status = getattr(annualneedex, 'status')
     an_complete = getattr(annualneedex, 'complete')
     request.session['current_annualneed_id'] = annualneedex.id


     context = {'year': year,'annualneed':annualneedex,'status':an_status,'complete':an_complete}
     return render(request,'main/pages/home.html',context)



################################################################################################################
##Pass Id of sepcific item/order :))))
@login_required(login_url='mainlogin')
@allowed_users(allowed_roles=['Normal-Users'])
def AddOrder(request,pk):
     Annualneed = AnnualNeed.objects.get(pk = pk)

     the_complete_status = getattr(Annualneed, 'complete')
     if(the_complete_status == True):
          print('The annual Need Is Confirmed')
          return redirect('main:userhome')
     
     orderform = OrderForm(initial = {'annualneed':Annualneed})
     #orderform = OrderForm(request.POST or None)

     if request.method == "POST":
          orderform = OrderForm(request.POST )
          if orderform.is_valid():
               order = orderform.save(commit=False)
               order.annualneed = Annualneed
               order.save()
          #      return redirect("main:OrderDetail", pk=order.id)
          # else:
          #      return render(request,'main/partials/Order-form.html',context = {'orderform':orderform})
     orders = Order.objects.filter(annualneed = Annualneed)

     context = {'orderform':orderform, 'Annualneed':Annualneed,'orders':orders}
     return render(request,'main/pages/order.html',context)


################################################################################################################
@login_required(login_url='mainlogin')
@allowed_users(allowed_roles=['Normal-Users'])
def vieww(request,pk):
     Annualneed = AnnualNeed.objects.get(pk = pk)
     orderform = OrderForm(initial = {'annualneed':Annualneed})

     
     orders = Order.objects.filter(annualneed = Annualneed)
     context = {'orderform':orderform, 'Annualneed':Annualneed,'orders':orders}
     return render(request,'main/pages/ordernew.html',context)

################################################################################################################
@login_required(login_url='mainlogin')
@allowed_users(allowed_roles=['Normal-Users'])
def add(request,pk):
     Annualneed = AnnualNeed.objects.get(pk = pk)
     orderform = OrderForm(initial = {'annualneed':Annualneed})


     if request.method == "POST":
          orderform = OrderForm(request.POST )
          if orderform.is_valid():
               order = orderform.save(commit=False)
               order.annualneed = Annualneed
               order.save()

     orders = Order.objects.filter(annualneed = Annualneed)
     context = {'orderform':orderform, 'Annualneed':Annualneed,'orders':orders}
     return render(request,'main/partials/Order-detail.html',context)


################################################################################################################   
@login_required(login_url='mainlogin')
@allowed_users(allowed_roles=['Normal-Users'])
def  AddOrderForm(request,anpk):
     Category = request.GET.get('tags')  #######get thecategory from the htmx div of the dropdownlist as a POST method
    
     orderform = OrderForm(initial = {'annualneed':anpk}) 
     if Category == "All Categories":
          items = Item.objects.all()
          
     else:
          items = Item.objects.filter(tagname = Category)
          orderform.fields["item"].queryset = Item.objects.filter(tagname=Category)  ####querysetting the filed item (filtering based on categorys)
     #items = Item.objects.all()

     context = {'orderform':orderform,'items':items,'Annualneedid':anpk}
     return render(request, 'main/partials/Order-form.html',context)


################################################################################################################
@login_required(login_url='mainlogin')
@allowed_users(allowed_roles=['Normal-Users'])
def OrderDetail(request, pk):
     order = Order.objects.get(id = pk)
     
     context = {'order':order}
     return render(request, 'main/partials/Order-detail.html',context)


################################################################################################################
@login_required(login_url='mainlogin')
@allowed_users(allowed_roles=['Normal-Users'])
def OrderUpdate(request, pk):
    order = Order.objects.get(id=pk)
    orderform = OrderForm(request.POST or None, instance=order)

    if request.method == "POST":
        if orderform.is_valid():
            orderform.save()
            return redirect("OrderDetail", pk=order.id)

    context = {
         "order":order,
        "orderform": orderform
    }

    return render(request, "main/partials/Order-form.html", context)


################################################################################################################
@login_required(login_url='mainlogin')
@allowed_users(allowed_roles=['Normal-Users'])
def OrderDelete(request,pk):
     order = get_object_or_404(Order, id=pk)
     annualneed = getattr(order, 'annualneed')

     if request.method == "POST":
          order.delete()

     orders = Order.objects.filter(annualneed=annualneed)
     context = {'orders':orders}
     return render(request,'main/partials/Order-detail.html',context)

################################################################################################################
@login_required(login_url='mainlogin')
@allowed_users(allowed_roles=['Normal-Users'])
def confirm(request,anpk):
     AnnualNeed.objects.filter(pk = anpk).update(complete=True)
     AnnualNeed.objects.filter(pk = anpk).update(status='Pending')

     return redirect('main:userhome')
     

################################################################################################################
@login_required(login_url='mainlogin')
@allowed_users(allowed_roles=['Normal-Users'])
def Archive(request):
     currentdjangouser_S = request.session['current_djangouser_id']
     a = User.objects.get(user = currentdjangouser_S)
     Annualneeds = AnnualNeed.objects.filter(status='Approved',user=a)

     context = {'annualneeds':Annualneeds,'user':a}
     return render(request, "main/pages/archive.html", context)
     

################################################################################################################
@login_required(login_url='mainlogin')
@allowed_users(allowed_roles=['Normal-Users'])
def ArchiveAN(request,pk):
     Annualneed = AnnualNeed.objects.get(pk=pk)
     Orders = Order.objects.filter(annualneed=Annualneed)

     context = {'annualneed':Annualneed,'orders':Orders}
     return render(request, "main/pages/AnnualNeedDoc.html", context)


################################################################################################################
@login_required(login_url='mainlogin')
@allowed_users(allowed_roles=['Normal-Users'])
def ANDoc2Alter(request,anpk):
     
     Annualneed = AnnualNeed.objects.get(pk=anpk)
     Annualneed.complete= False
     Annualneed.save()


     OrderswithCommnets = Order.objects.exclude(comment__isnull=True)
     context = {'Annualneed':Annualneed,'orders':OrderswithCommnets}
     return render(request, "main/pages/Doc2bAltered.html", context)


################################################################################################################
@login_required(login_url='mainlogin')
def Export_Excel(request,pk):
     Annualneed = AnnualNeed.objects.get(pk=pk)
     response = HttpResponse(content_type= 'application/ms-excel')
     response['Content-Disposition']= 'attachment; filename=AnnualNeed' + \
          str(Annualneed.yearofdoc()) + '.xls'

     wb = xlwt.Workbook(encoding= 'utf-8')
     ws = wb.add_sheet('Orders')
     row_num = 0
     font_style = xlwt.XFStyle()
     font_style.font.bold = True  ######header

     columns = ['item name',
               'Total Quantity',
               'First Semester',
               'Second Semester',
               'Third Semester',
               'Description',
               'First Brand',
               'Second Brand',
               'Third Brand',
               'FlowRate',
               'Unit',
               'Sigle Approximate Price'
               ]
     
     for col_num in range(len(columns)):
          ws.write(row_num,col_num,columns[col_num],font_style)

     font_style = xlwt.XFStyle()

     ###dynamic
     rows = Order.objects.filter(annualneed = Annualneed).values_list(
               'item',
               'Total',
               'FirstSemsQuantity',
               'SecondSemsQuantity',
               'ThirdSemsQuantity',
               'Description',
               'FirstBrand',
               'SecondBrand',
               'ThirdBrand',
               'FlowRate',
               'Unit',
               'ApproxPrice')

     for row in rows:
          row_num+= 1

          for col_num in range(len(row)):
               ws.write(row_num,col_num, str(row[col_num]),font_style)

     wb.save(response)
     return response


################################################################################################################
@login_required(login_url='mainlogin')
@allowed_users(allowed_roles=['Normal-Users'])
def Update(request, pk):
     order = get_object_or_404(Order, pk=pk)
     annualneed = getattr(order, 'annualneed')

     form = OrderForm(request.POST or None, instance=order)

     if request.method == 'POST':
          if form.is_valid():
               form.save()
               return redirect('main:AddOrder' ,pk = annualneed.pk)


     context = {'order':form, 'Annualneedid':annualneed.id}
     return render(request, 'main/pages/OrderUpdate.html',context = context)

################################################################################################################
@login_required(login_url='mainlogin')
@allowed_users(allowed_roles=['Normal-Users'])
def Update2b(request, pk):
     order = get_object_or_404(Order, pk=pk)
     orderid = pk
     comment = getattr(order, 'comment')

     annualneed = getattr(order, 'annualneed')
     form = OrderForm(request.POST or None, instance=order)

     if request.method == 'POST':
          if form.is_valid():
               form.save()
               return redirect('main:ANDoc2Alter' ,anpk = annualneed.pk)

     annualneed_status = getattr(annualneed, 'status')
     context = {'order':form, 'Annualneedid':annualneed.id,'status':annualneed_status ,'comment':comment,"orderid":orderid}
     return render(request, 'main/pages/OrderUpdate.html',context = context)


################################################################################################################
@login_required(login_url='mainlogin')
@allowed_users(allowed_roles=['Normal-Users'])
def Deleteorder(request,pk):
     order = get_object_or_404(Order, id=pk)
     annualneed = getattr(order, 'annualneed')

     if request.method == "POST":
          order.delete()


     return redirect('main:ANDoc2Alter' ,anpk = annualneed.pk)


def template(request,pk):
     orders = Order.objects.filter(annualneed = pk)
     current_annualneed_id = request.session['current_annualneed_id']
     current_annualneed = AnnualNeed.objects.get(id=current_annualneed_id)

     if (getattr(current_annualneed, 'complete')):
          print("Annual Need Already Confirmed. You Can't Edit On It")
     else:
          for order in orders:
               test = order
               test.pk = None
               test.annualneed = current_annualneed
               test.save()


     return redirect('main:AddOrder',pk = current_annualneed_id)
     


     
