from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('<int:order_id>/', views.order, name='order'),
    path('create_order/', views.create_order, name='create_order'),
    path('coupon/<int:order_id>', views.coupon, name='coupon'),
]