from django.db import models
from django.contrib.auth.models import User
from home.models import *
from django.forms import ModelForm


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    create = models.DateTimeField(auto_now_add=True)
    discount = models.IntegerField(blank=True, null=True)
    paid = models.BooleanField(default=False)
    f_name = models.CharField(max_length=200)
    l_name = models.CharField(max_length=200)
    email = models.EmailField()
    address = models.CharField(max_length=1000)

    def __str__(self):
        return self.user.username

    def get_price(self):
        price = sum(i.price() for i in self.order_item.all())
        if self.discount:
            total = (self.discount / 100) * price
            return int(price - total)
        return price


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_item')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField()

    def __str__(self):
        return self.user.username

    def price(self):
        if self.product.status != 'None':
            return self.variant.total_price * self.quantity
        else:
            return self.product.total_price * self.quantity


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['f_name', 'l_name', 'email', 'address']


class Coupon(models.Model):
    code = models.CharField(max_length=200, unique=True)
    active = models.BooleanField(default=False)
    start = models.DateTimeField()
    end = models.DateTimeField()
    discount = models.IntegerField()
