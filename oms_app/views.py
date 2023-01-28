from tabnanny import check
from django.shortcuts import render ,redirect
from main.models import *
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate , login ,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from .forms import *
from django.http import HttpResponseRedirect ,HttpResponse
from django.contrib import messages
from main.decorators import *


# Create your views here.


#@login_required
# def LogIn(request):
#      if request.method=='POST':
#           username = request.POST.get('username')
#           password = request.POST.get('password')

#           user = authenticate(request ,username=username ,password=password)
#           if user is not None:
#                login(request , user)
#                return redirect('adminhome')
#           else:
#                messages.info(request, 'username or password is incorrect')
#      return render(request,'oms_app/pages/login.html')

@login_required(login_url='mainlogin')
def LogOut(request):
     logout(request)
     return redirect('mainlogin')

@login_required(login_url='mainlogin')
@allowed_users(allowed_roles=['Vice-President'])
def documents(request):
     orders=Order.objects.filter(annualneed__status="Pending")
     context={
          'orders':orders, }     
     return render(request,'pages/pendingdocuments.html',context)


@login_required(login_url='mainlogin')
@allowed_users(allowed_roles=['Vice-President'])
def adminhome(request):
     pendingannualneed=AnnualNeed.objects.filter(status='Pending',complete=True).count()
     approvedannualneed=AnnualNeed.objects.filter(status='Approved').count()
     items=Item.objects.count()

     annualneeds_pendeing=AnnualNeed.objects.filter(status='Pending',complete=True).count()
     annualneeds_Approved=AnnualNeed.objects.filter(status='Approved').count()
     boolan=False
     if int(annualneeds_pendeing)==0 and int(annualneeds_Approved)!=0 :
          boolan=True

     context={ 'Pannualneed': pendingannualneed,
               'Aannualneed': approvedannualneed,
               'allitems':items,
               'boolan':boolan }
     return render(request,'oms_app/pages/adminhome.html',context)


@login_required(login_url='mainlogin')
@allowed_users(allowed_roles=['Vice-President'])
def annualneedspending(request):
     annualneeds=AnnualNeed.objects.filter(status='Pending',complete=True).order_by('-YearDate')
     
     context={
          'annualneeds':annualneeds,
     }

     return render(request,'oms_app/pages/annualneedspending.html',context)


@login_required(login_url='mainlogin')
@allowed_users(allowed_roles=['Vice-President'])
def annualneedspendingrp(request,id):
     annualneed =AnnualNeed.objects.get(id=id)
     annualneedorders=annualneed.order_set.all()
    
     context={ 
          'annualneed':annualneed ,
          'annualneedorders':annualneedorders,
     }
     return render(request,'oms_app/pages/pendingdocuments.html',context)


@login_required(login_url='mainlogin')
@allowed_users(allowed_roles=['Vice-President'])
def annualneedsapproved(request):
     annualneeds=AnnualNeed.objects.filter(status='Approved').order_by('-YearDate')
     context={
         'annualneeds':annualneeds 
        
     }
     return render(request,'oms_app/pages/annualneedsapproved.html',context)


@login_required(login_url='mainlogin')
@allowed_users(allowed_roles=['Vice-President'])
def annualneedsapprovedrp(request,id):
      annualneed =AnnualNeed.objects.get(id=id)
      annualneedorders=annualneed.order_set.all() 
      context={ 
          'annualneed':annualneed ,
          'annualneedorders':annualneedorders
      }
      return render(request,'oms_app/pages/approveddocuments.html',context)

 

@login_required(login_url='mainlogin')
@allowed_users(allowed_roles=['Vice-President'])
def ApprovedOrder(request,id):
     annualneed =AnnualNeed.objects.get(id=id)
     annualneed.status ='Approved'
     annualneed.save()

     return redirect('adminhome')   
     #return render(request,'oms_app/pages/adminhome.html',context)


@login_required(login_url='mainlogin')
@allowed_users(allowed_roles=['Vice-President'])
def stock(request):
     return render(request,'oms_app/pages/stock.html')   


@login_required(login_url='mainlogin')
@allowed_users(allowed_roles=['Vice-President'])
def stockitems(request,tg):
     items=Item.objects.filter(tagname=tg)
     context={
          'items':items,
          'tg':tg
     }
     return render(request,'oms_app/pages/stockitems.html',context)   


@login_required(login_url='mainlogin')
@allowed_users(allowed_roles=['Vice-President'])
def searchitem(request):
     if request.method == "POST" :
          searched =request.POST['searched']
          items = Item.objects.filter(ItemName__contains = searched )
          if items:
               context ={
               'searched':searched ,
               'items':items
               }
               return render(request,'oms_app/pages/search.html',context)
          else:
               msg ='item not found'
               context={
               'msg':msg
               } 
               return render(request,'oms_app/pages/search.html',context) 
     else:           
          return render(request,'/')  
          


@login_required(login_url='mainlogin')
@allowed_users(allowed_roles=['Vice-President'])
def stockchart(request):
      allitems={}
      mostrequested={}    
      graterthan =request.POST['graterthan'] 
      for annualneed in AnnualNeed.objects.all():
           for order in annualneed.order_set.all():
                if order.item in allitems :
                     allitems[order.item]+=1
                else:
                     allitems[order.item]=1
      for i in allitems:
            if allitems[i]>int(graterthan):
                 mostrequested[i]=allitems[i] 
      context ={
               'allitems':allitems,
               'mostrequested':mostrequested,
          }
      return render(request,'oms_app/pages/stockchart.html',context)    


@login_required(login_url='mainlogin')
@allowed_users(allowed_roles=['Vice-President'])
def stockleastreq(request):
      allitems={}
      leastrequested={}
      lessthan =request.POST['lessthan'] 
      for annualneed in AnnualNeed.objects.all():
           for order in annualneed.order_set.all():
                if order.item in allitems :
                     allitems[order.item]+=1
                else:
                     allitems[order.item]=1
      for i in allitems:
            if allitems[i]<int(lessthan):
                 leastrequested[i]=allitems[i]
  
      context ={
               'allitems':allitems,
               'leastrequested':leastrequested
          }
      return render(request,'oms_app/pages/stockleastreq.html',context)  


@login_required(login_url='mainlogin')
@allowed_users(allowed_roles=['Vice-President'])
def neverrequesteditems(request):
      allitems={}
      neverrequesteditems={}
      
      
      for annualneed in AnnualNeed.objects.all():
           for order in annualneed.order_set.all():
                if order.item.ItemName in allitems :
                     allitems[order.item.ItemName]+=1
                else:
                     allitems[order.item.ItemName]=1                    

      for j in Item.objects.all():
                if j.ItemName  in  allitems:
                     None
                else: 
                     neverrequesteditems[j.id]= j
            



      context ={
               'allitems':allitems,
               'neverrequesteditems':neverrequesteditems
          }
      return render(request,'oms_app/pages/neverrequesteditems.html',context)  


@login_required(login_url='mainlogin')
@allowed_users(allowed_roles=['Vice-President'])
def approveditems(request):
     #Aggregation

     allitems={}  
     check={}  
     onlyrepeateditems={} 
     annualneeds = {}
     ordersobj = {}

     for annualneed in AnnualNeed.objects.filter(status='Approved',YearDate__year=2022):
          annualneeds[annualneed]= annualneed

          for order in annualneed.order_set.all():
               ordersobj[order] = order
               if order.item.ItemName in allitems :
                   allitems[order.item.ItemName]+=order.Total
                   check[order.item.ItemName]=True

               else:
                   check[order.item.ItemName]=False
                   allitems[order.item.ItemName]=order.Total 


     for i in allitems :
          if check[i]==True:
               onlyrepeateditems[i]=allitems[i]
          else:
               None
     context={
          'onlyrepeateditems':onlyrepeateditems,
          'allitems':allitems,
          'annualneeds':annualneeds,
          'ordersobj':ordersobj
     }       
     return render(request,'oms_app/pages/approveditems.html',context)


@login_required(login_url='mainlogin')
@allowed_users(allowed_roles=['Vice-President'])
def needsalteration(request,id):
     check_comment = False
     annualneed =AnnualNeed.objects.get(id=id)
     for order in annualneed.order_set.all():
          if order.comment != None:
               check_comment = True
               annualneed.status ='Needs Alteration'
               annualneed.complete =True
               annualneed.save()
               break               

     if check_comment:
          return redirect('annualneeds')
     else:
          messages.error(request, 'You Have To Add At Least One Comment To Resend This Annualneed To User')
          return redirect('/pendingdocuments/'+str(annualneed.id)+'/')



@login_required(login_url='mainlogin')
@allowed_users(allowed_roles=['Vice-President'])
def  approve(request):

     allitems={}  
     check={}  
     onlyrepeateditems={} 
     
     for annualneed in AnnualNeed.objects.filter(status='Approved'):
          for order in annualneed.order_set.all():
                if order.item.ItemName in allitems :
                     allitems[order.item.ItemName]=allitems[order.item.ItemName]+order.Total_Quantity()
                     check[order.item.ItemName]=True
                else:
                     check[order.item.ItemName]=False
                     allitems[order.item.ItemName]=order.Total_Quantity()

     for i in allitems :
          if check[i]==True:
               onlyrepeateditems[i]=allitems[i]
          else:
               None
     old_Total = None
     if request.method=='POST':
          item = request.POST['dropdown']
          approvedquantity =request.POST['approvedquantity'] 
          #distribution
          for annualneed in AnnualNeed.objects.filter(status='Approved'):
               for order in annualneed.order_set.all():
                    if order.item.ItemName in  allitems:
                         if item == order.item.ItemName:
                              old_Total= order.Total_Quantity()
                              order.Total = order.Total_Quantity()
                              perc= (int(approvedquantity)/int(allitems[item]))
                             #####resetting total quantity for specif item
                              order.Total= perc * order.Total
                              new_total=order.Total
                              order.save()
                              SemesterDis(new_total,old_Total,order.item.id,annualneed.id)

                    else:
                         None
     return redirect('approveditems')


@login_required(login_url='mainlogin')
@allowed_users(allowed_roles=['Vice-President'])
def SemesterDis(NewTotal,OldTotal,itemm,annualneedd):

     annualneed = AnnualNeed.objects.get(id=annualneedd)
     order = Order.objects.get(item = itemm, annualneed = annualneedd )
     ##percentage 
     order.FirstSemsQuantity = (order.FirstSemsQuantity/OldTotal) * NewTotal
     order.SecondSemsQuantity = (order.SecondSemsQuantity/OldTotal) * NewTotal
     order.ThirdSemsQuantity = (order.ThirdSemsQuantity/OldTotal) * NewTotal
     order.save()


@login_required(login_url='mainlogin')
@allowed_users(allowed_roles=['Vice-President'])
def addcomment(request):
     if request.method=="POST":
               order = request.POST['dropdown']
               comment = request.POST['comment']
               order = Order.objects.get(id =order)
               order.comment = comment
               order.save()
               return redirect('annualneedspendingrp', id = order.annualneed.id)

#@login_required(login_url='mainlogin')
#@allowed_users(allowed_roles=['Vice-President'])
def approveditemswithfilledinfo(request,i):
     #Aggregation
     allitems={}  
     check={}  
     onlyrepeateditems={} 
     annualneeds = {}
     ordersobj = {}
     orderobj = Order.objects.get(id = i)
     orderid= i
     if request.method=='POST':
          orderobj.FirstSemsQuantity =int(request.POST['FirstSemQuantity'])
          orderobj.SecondSemsQuantity =int(request.POST['SecondSemQuantity'])
          orderobj.ThirdSemsQuantity =int(request.POST['ThirdSemQuantity'])
          orderobj.Total= orderobj.Total_Quantity()
          orderobj.save()
          return redirect('approveditems') 
     
     for annualneed in AnnualNeed.objects.filter(status='Approved',YearDate__year=2022):
          annualneeds[annualneed]= annualneed

          for order in annualneed.order_set.all():
               ordersobj[order] = order
               if order.item.ItemName in allitems :
                   allitems[order.item.ItemName]+=order.Total
                   check[order.item.ItemName]=True

               else:
                   check[order.item.ItemName]=False
                   allitems[order.item.ItemName]=order.Total 


     for i in allitems :
          if check[i]==True:
               onlyrepeateditems[i]=allitems[i]
          else:
               None
      
     context={
          'onlyrepeateditems':onlyrepeateditems,
          'allitems':allitems,
          'annualneeds':annualneeds,
          'ordersobj':ordersobj, 
          'obj':orderobj,
          'orderid':orderid
     }  
     return render(request,'oms_app/pages/approveditems.html',context)
