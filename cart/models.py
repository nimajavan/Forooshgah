from django.db import models
from django.forms import ModelForm
from home.models import *


class Card(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.PositiveIntegerField()


class CardForm(ModelForm):
    class Meta:
        model = Card
        fields = ['quantity']
