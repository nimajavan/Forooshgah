from django.shortcuts import render, redirect
from .models import *
from cart.models import Card
from .forms import CouponForm
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.contrib import messages



def order(request, order_id):
    order_ob = Order.objects.get(id=order_id)
    form = CouponForm()
    context = {'order_ob': order_ob, 'form': form}
    return render(request, 'order/order.html', context)


def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            order_ = Order.objects.create(user_id=request.user.id, f_name=data['f_name'], l_name=data['l_name'],
                                          email=data['email'], address=data['address'])
            card = Card.objects.filter(user_id=request.user.id)
            for c in card:
                OrderItem.objects.create(user_id=request.user.id, order_id=order_.id, product_id=c.product_id,
                                         variant_id=c.variant_id, quantity=c.quantity)
            return redirect('order:order', order_.id)


@require_POST
def coupon(request, order_id):
    form_coupon = CouponForm(request.POST)
    time = timezone.now()
    if form_coupon.is_valid():
        data = form_coupon.cleaned_data['code']
        try:
            copon = Coupon.objects.get(code__iexact=data, start__lte=time, end__gte=time, active=True)
        except Coupon.DoesNotExist:
            messages.error(request, 'this coupon dose not exist', 'danger')
            return redirect('order:order', order_id)
        order = Order.objects.get(id=order_id)
        order.discount = copon.discount
        order.save()
    return redirect('order:order', order_id)

