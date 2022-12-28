from django.urls import path
from . import views

app_name = 'cart'
urlpatterns = [
    path('', views.card, name='card'),
    path('add_cart/<int:id>', views.add_cart, name='add_cart'),
    path('remove_cart/<int:id>', views.remove_cart, name='remove_cart'),
    path('add_quantity/<int:id>', views.add_quantity, name='add_quantity'),
    path('remove_quantity/<int:id>', views.remove_quantity, name='remove_quantity'),
]
