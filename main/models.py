from django.db import models
from django.contrib.auth.models import User
import datetime

from django.db.models.fields.related import OneToOneField

RequestingParty = (
                    ('IT','IT'),
                    ('ARCHITECTURE','ARCHITECTURE'),
                    ('MEDICINE','MEDICINE'),
                    ('PHARMACY','PHARMACY'),
                    ('DENTISTRY','DENTISTRY'),
                    ('BUSINESS','BUSINESS'),

                )
# Create your models here.

def current_year():
    return datetime.date.year().year


class User(models.Model): 
    user = OneToOneField(User,on_delete=models.SET_NULL,null = True, blank=True)
    Name = models.CharField(max_length=50)
    Email = models.CharField(max_length=100)
    RequestingParty =  models.CharField(max_length =60, null = True, choices =RequestingParty)
    def __str__(self):
     return self.Name

class Stock(models.Model):
    StockName = models.CharField(max_length=50)

class Item(models.Model):
    ItemName =models.CharField(max_length=50)
    Tags = (
                    ('General','General'),
                    ('Medical','Medical'),
                    ('IT','IT'),
                    ('Engineering','Engineering'),
                )
    Quantity = models.PositiveIntegerField(default=1)
    Description = models.CharField(max_length=150, null = True, blank = True)
    Brand = models.CharField(max_length=50, null = True, blank = True)
    tagname = models.CharField(max_length =200, null = True, choices =Tags)
    stock =models.ForeignKey(Stock, on_delete=models.CASCADE)

    def __str__(self):
        return self.ItemName

        
class AnnualNeed(models.Model):
    Statuss = (
                    ('Pending','Pending'),
                    ('Being Reviewed','Being Reviewed'),
                    ('Needs Alteration','Needs Alteration'),
                    ('Approved','Approved'),
                )
 
    YearDate=models.DateField()
    status = models.CharField(max_length =200, null = True, choices = Statuss, default='Pending')
    complete = models.BooleanField(default=False)
    RequestingParty = models.CharField(max_length =200, null = True, blank=True, choices =RequestingParty)
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null = True, blank=True)

    def yearofdoc(self):
        return self.YearDate.strftime('%Y')

    def __str__(self):
     return self.RequestingParty + " Document For Year " + str(self.YearDate.strftime('%Y'))


class Order(models.Model):
    
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    FirstSemsQuantity=models.PositiveIntegerField()
    SecondSemsQuantity=models.PositiveIntegerField()
    ThirdSemsQuantity=models.PositiveIntegerField()
    Total = models.PositiveIntegerField(default=0, null = True, blank = True)
    Description = models.CharField(max_length=150, null = True, blank = True)
    FirstBrand = models.CharField(max_length=50, null = True, blank = True)
    SecondBrand = models.CharField(max_length=50, null = True, blank = True)
    ThirdBrand = models.CharField(max_length=50, null = True, blank = True)
    FlowRate = models.CharField(max_length=100, null = True, blank = True)
    Unit = models.CharField(max_length=100, null = True, blank = True)
    ApproxPrice = models.FloatField()
    annualneed = models.ForeignKey(AnnualNeed, on_delete=models.CASCADE, null=False)
    comment = models.CharField(max_length=200, null = True, blank = True)

    def __str__(self):
     return self.item.ItemName + " " +str(self.annualneed.RequestingParty)
    
    def total_Approx_Price(self):
        if(self.ApproxPrice):
            return self.ApproxPrice * (self.FirstSemsQuantity +self.SecondSemsQuantity+self.ThirdSemsQuantity)
        else:
            return 0

    def Total_Quantity(self):
        total = 0
        if(self.FirstSemsQuantity!=None):
            total+= self.FirstSemsQuantity
        if(self.SecondSemsQuantity!=None):
            total+= self.SecondSemsQuantity
        if(self.ThirdSemsQuantity!=None):
            total+= self.ThirdSemsQuantity
        self.Total = total
        return total
        


