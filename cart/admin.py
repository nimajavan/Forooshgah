from django.contrib import admin
from .models import *


class CardAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'variant', 'quantity',]


admin.site.register(Card, CardAdmin)
