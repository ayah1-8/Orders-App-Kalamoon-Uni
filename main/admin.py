from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Order)
#admin.site.register(AnnualNeed)
admin.site.register(Stock)
admin.site.register(Item)
admin.site.register(User)

class OrderInlineAdmin(admin.TabularInline):
    model = Order

class AnnualNeedAdmin(admin.ModelAdmin):
    inlines = [OrderInlineAdmin]

admin.site.register(AnnualNeed,AnnualNeedAdmin)

