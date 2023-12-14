from django.contrib import admin

from orders.models import Order, OrderStatus, Payment, AppliedPromoCode, TransportCompany


# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_price', 'date_created', 'status')



admin.site.register(Order, OrderAdmin)
admin.site.register(OrderStatus)
admin.site.register(Payment)
admin.site.register(AppliedPromoCode)
admin.site.register(TransportCompany)