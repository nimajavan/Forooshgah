from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import *
from .forms import *
from django.db.models import Q, Max, Min
from cart.models import *
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from .filters import ProductFilter


def home(request):
    category = Category.objects.filter(sub_cat=False)
    return render(request, 'home/home.html', {'category': category})


def products(request, slug=None, id=None):
    product = Products.objects.all()
    min = Products.objects.aggregate(unit_price=Min('unit_price'))
    min_price = int(min['unit_price'])
    max = Products.objects.aggregate(unit_price=Max('unit_price'))
    max_price = int(max['unit_price'])
    filter_product = ProductFilter(request.GET, queryset=product)
    product = filter_product.qs
    paginator = Paginator(product, 2)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    search = SearchForm()
    category = Category.objects.filter(sub_cat=False)
    if slug and id:
        data = Category.objects.get(slug=slug, id=id)
        page_obj = Products.objects.filter(category=data)
        paginator = Paginator(page_obj, 2)
        page_num = request.GET.get('page')
        page_obj = paginator.get_page(page_num)

    return render(request, 'home/product.html', {'product': page_obj, 'category': category, 'search': search
        , 'filter': filter_product, 'min': min_price, 'max': max_price})


def products_details(request, id):
    comment_form = CommentForm()
    p_image = Image.objects.filter(product_id=id)
    com_rep = ReplyForm()
    card_form = CardForm()
    product_ = Products.objects.get(id=id)
    comments = Comment.objects.filter(product_id=id, is_reply=False)
    similar = product_.tags.similar_objects()[:2]
    ip = request.META.get('REMOTE_ADDR')
    view = View.objects.filter(product_id=product_.id, ip=ip)
    if not view.exists():
        View.objects.create(ip=ip, product_id=product_.id)
        product_.views += 1
        product_.save()
    is_like = False
    if product_.like.filter(id=request.user.id).exists():
        is_like = True
    else:
        is_like = False
    is_unlike = False
    if product_.unlike.filter(id=request.user.id).exists():
        is_unlike = True
    else:
        is_unlike = False
    if product_.status != 'None':
        if request.method == 'POST':
            variant = Variant.objects.filter(product_variant_id=id)
            var_id = request.POST.get('select')
            variants = Variant.objects.get(id=var_id)
        else:
            variant = Variant.objects.filter(product_variant_id=id)
            variants = Variant.objects.get(id=variant[0].id)
        context = {'product': product_, 'variants': variants, 'variant': variant, 'similar': similar, 'is_like': is_like
            , 'is_unlike': is_unlike, 'comment_form': comment_form, 'comments': comments, 'com_rep': com_rep,
                   'image': p_image, 'card_form': card_form}
        return render(request, 'home/details.html', context)
    else:
        return render(request, 'home/details.html', {'product': product_, 'similar': similar, 'is_like': is_like,
                                                     'is_unlike': is_unlike, 'comment_form': comment_form,
                                                     'comments': comments, 'com_rep': com_rep, 'image': p_image,
                                                     'card_form': card_form})


def product_like(request, id):
    url = request.META.get('HTTP_REFERER')
    product = get_object_or_404(Products, id=id)
    if product.like.filter(id=request.user.id).exists():
        product.like.remove(request.user)
    else:
        product.like.add(request.user)
        messages.success(request, 'thank you for like', 'success')
    return redirect(url)


def product_unlike(request, id):
    url = request.META.get('HTTP_REFERER')
    product = get_object_or_404(Products, id=id)
    if product.unlike.filter(id=request.user.id).exists():
        product.unlike.remove(request.user)
    else:
        product.unlike.add(request.user)
        messages.success(request, 'thank you for unlike', 'success')
    return redirect(url)


def comment(request, id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            data = comment_form.cleaned_data
            Comment.objects.create(text=data['text'], rate=data['rate'], user_id=request.user.id, product_id=id)
        return redirect(url)


def comment_reply(request, id, text_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        reply_form = ReplyForm(request.POST)
        if reply_form.is_valid():
            data = reply_form.cleaned_data
            Comment.objects.create(text=data['text'], product_id=id, reply_id=text_id, user_id=request.user.id,
                                   is_reply=True)
            messages.success(request, 'thanks for reply')
        return redirect(url)


def comment_likes(request, id):
    url = request.META.get('HTTP_REFERER')
    comment_lik = Comment.objects.get(id=id)
    if comment_lik.comment_like.filter(id=request.user.id).exists():
        comment_lik.comment_like.remove(request.user)
    else:
        comment_lik.comment_like.add(request.user)
    return redirect(url)


def product_search(request):
    product = Products.objects.all()
    if request.method == 'POST':
        search = SearchForm(request.POST)
        if search.is_valid():
            data = search.cleaned_data['search']
            if data is not None:
                if data.isdigit():
                    product = product.filter(Q(unit_price=data))
                else:
                    product = product.filter(Q(name__icontains=data))
            return render(request, 'home/product.html', {'product': product, 'search': search})


def contact_us(request):
    if request.method == 'POST':
        name = request.POST['subject']
        email = request.POST['email']
        msg = request.POST['message']
        body = name + '\n' + email + '\n' + msg
        form = EmailMessage(
            'contact us',
            body,
            'test',
            ('nimajavangt@gmail.com',),
        )
        form.send(fail_silently=False)
        messages.success(request, 'thanks for contact us', 'info')
    return render(request, 'home/contact.html')
