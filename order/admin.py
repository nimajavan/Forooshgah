from django.contrib import admin
from .models import *


class ItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ['user', 'product', 'variant', 'quantity', 'price']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'create', 'paid', 'f_name', 'l_name', 'email', 'address', 'get_price']
    inlines = [ItemInline]


class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'start', 'end', 'active', 'discount']


admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(Coupon, CouponAdmin)
admin.site.register(Chart)
