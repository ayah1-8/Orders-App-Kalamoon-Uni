from django.urls import path
from . import views

app_name = 'main'


urlpatterns =[

    #path('login/',views.loginPage, name='login'),
    path('UserHome/',views.HomeUser, name='userhome'), #### select type of documnet to add
    path('Order/<pk>/', views.AddOrder, name='AddOrder'),

    #path('ajax/AddTestOrder/<pk>/', views.Test, name='Test'),
    #path('ajax/UpdateOrder/<pk>/', views.product_update, name='Order-Update'),

    path('OrderNEW/<pk>/', views.vieww, name='AddOrdernew'),
    path('htmx/OrderNEW/<pk>/', views.add, name='add'),
    path('htmx/order/<anpk>',views.AddOrderForm, name='OrderForm'),
    path('htmx/order/<pk>', views.OrderDetail, name='OrderDetail'),
    #path('htmx/order/<pk>/update/', views.OrderUpdate, name="OrderUpdate"),
    path('order/<pk>/update/', views.Update, name="OrderUpdate"),
    path('order2b/<pk>/update/', views.Update2b, name="OrderUpdate2b"),
    path('htmx/order/<pk>/delete/', views.OrderDelete, name="OrderDelete"),
    path('order/<pk>/delete/', views.Deleteorder, name="deleteorder"),


    path('Archive/',views.Archive, name='Archive'), 
    path('Archive/<pk>',views.ArchiveAN, name='ArchiveAN'), 
    path('DoctbAltered/<anpk>',views.ANDoc2Alter, name='ANDoc2Alter'), 
    path('Template/<pk>',views.template, name='template'), 

    
	path('Confirm/<anpk>', views.confirm, name="Confirm"),  
	path('Exportxls/<pk>', views.Export_Excel, name="export"),  
	path('logout/', views.logoutUser, name="logout"),  

    
]