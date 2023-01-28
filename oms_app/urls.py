from django.urls import path
from . import views
urlpatterns =[
    #path('loginvp/',views.LogIn, name='login'),
    path('',views.LogOut, name='LogOut'),
    path('adminhome/',views.adminhome, name='adminhome'),
    path('annualneeds/',views.annualneedspending, name='annualneeds'),
    path('approvedannualneeds/',views.annualneedsapproved, name='annualneedsapproved'),
    path('pendingdocuments/<int:id>/',views.annualneedspendingrp, name='annualneedspendingrp'),
    path('approveddocuments/<int:id>/',views.annualneedsapprovedrp, name='annualneedsapprovedrp'),
    path('adminhome/<int:id>/',views.ApprovedOrder, name='ApprovedOrder'),
    path('stock/',views.stock, name='stock'),
    path('items/<str:tg>/',views.stockitems, name='stockitems'),
    path('searchitem/',views.searchitem, name='searchitem'),
    path('stockchart/',views.stockchart, name='stockchart'),
    path('stockleastreq/',views.stockleastreq, name='stockleastreq'),
    path('neverrequesteditems/',views.neverrequesteditems, name='neverrequesteditems'),
    path('annualneeds/<int:id>/',views.needsalteration, name='needsalteration'),
    path('approveditems/',views.approveditems, name='approveditems'),
    path('approveditems/<i>',views.approveditemswithfilledinfo, name='approveditems1'),
    path('approvequantities/',views.approve, name='approvequantities'),
    path('addcomment/',views.addcomment, name='addcomment'),
] 
  