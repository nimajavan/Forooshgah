from django.shortcuts import render, redirect
from .models import *
from order.models import OrderForm


def card(request):
    card_ = Card.objects.filter(user_id=request.user.id)
    order = OrderForm()
    total = 0
    for p in card_:
        if p.product.status != 'None':
            total += p.variant.total_price * p.quantity
        else:
            total += p.product.total_price * p.quantity
    return render(request, 'cart/cart.html', {'card': card_, 'total': total, 'order': order})


def add_cart(request, id):
    product = Products.objects.get(id=id)
    if product.status != 'None':
        var_id = request.POST.get('select')
        data = Card.objects.filter(user_id=request.user.id, variant_id=var_id)
        if data:
            check = 'yes'
        else:
            check = 'no'
    else:
        data = Card.objects.filter(user_id=request.user.id, product_id=id)
        if data:
            check = 'yes'
        else:
            check = 'no'
    if request.method == 'POST':
        url = request.META.get('HTTP_REFERER')
        form = CardForm(request.POST)
        var_id = request.POST.get('select')
        if form.is_valid():
            info = form.cleaned_data['quantity']
            if check == 'yes':
                if product.status != 'None':
                    shop = Products.objects.get(user_id=request.user.id, product_id=id, variant_id=var_id)
                else:
                    shop = Products.objects.get(user_id=request.user.id, product_id=id)
                shop.quantity += info
                shop.save()
            else:
                Card.objects.create(user_id=request.user.id, product_id=id, variant_id=var_id, quantity=info)
        return redirect(url)


def remove_cart(request, id):
    url = request.META.get('HTTP_REFERER')
    Card.objects.filter(id=id).delete()
    return redirect(url)


def add_quantity(request, id):
    url = request.META.get('HTTP_REFERER')
    cart = Card.objects.get(id=id)
    if cart.product.status == 'None':
        product = Products.objects.get(id=cart.product.id)
        if product.amount > cart.quantity:
            cart.quantity += 1
    else:
        variant = Variant.objects.get(id=cart.variant.id)
        if variant.amount > cart.quantity:
            cart.quantity += 1
    cart.save()
    return redirect(url)


def remove_quantity(request, id):
    url = request.META.get('HTTP_REFERER')
    cart = Card.objects.get(id=id)
    product = Products.objects.get(id=cart.product.id)
    if cart.quantity > 0:
        cart.quantity -= 1
        cart.save()
    if cart.quantity == 0:
        cart.delete()
    return redirect(url)
