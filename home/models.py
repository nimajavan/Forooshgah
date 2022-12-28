from django.db import models
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.db.models.signals import post_save


class Category(models.Model):
    sub_category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='sub')
    sub_cat = models.BooleanField(default=False)
    name = models.CharField(max_length=200)
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    slug = models.SlugField(allow_unicode=True, unique=True, blank=True, null=True)
    image = models.ImageField(upload_to='category', null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('home:category', args=[self.slug, self.id])


class Products(models.Model):
    VARIANT = (
        ('None', 'none'),
        ('Size', 'size'),
        ('Color', 'color'),
    )
    category = models.ManyToManyField(Category, blank=True)
    name = models.CharField(max_length=200)
    amount = models.PositiveIntegerField()
    unit_price = models.PositiveIntegerField()
    discount = models.PositiveIntegerField(blank=True, null=True)
    change = models.BooleanField(default=False)
    total_price = models.PositiveIntegerField()
    information = RichTextUploadingField(blank=True, null=True)
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    available = models.BooleanField(default=True)
    tags = TaggableManager(blank=True)
    status = models.CharField(max_length=200, null=True, blank=True, choices=VARIANT, default=None)
    image = models.ImageField(upload_to='products')
    like = models.ManyToManyField(User, blank=True, related_name='product_like')
    total_like = models.IntegerField(default=0)
    unlike = models.ManyToManyField(User, blank=True, related_name='product_unlike')
    total_unlike = models.IntegerField(default=0)
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE, null=True, blank=True)
    color = models.ManyToManyField('Color', blank=True)
    size = models.ManyToManyField('Size', blank=True)
    views = models.IntegerField(default=0, null=True, blank=True)

    def total_like(self):
        return self.like.count()

    def total_unlike(self):
        return self.unlike.count()

    def __str__(self):
        return self.name

    @property
    def total_price(self):
        if not self.discount:
            return self.unit_price
        if self.discount:
            total = (self.discount * self.unit_price) / 100
            return int(self.unit_price - total)
        return self.total_price


class Size(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name


class Variant(models.Model):
    name = models.CharField(max_length=200)
    product_variant = models.ForeignKey(Products, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, null=True, blank=True)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.PositiveIntegerField()
    unit_price = models.PositiveIntegerField()
    discount = models.PositiveIntegerField(blank=True, null=True)
    total_price = models.PositiveIntegerField()

    def __str__(self):
        return self.name

    @property
    def total_price(self):
        if not self.discount:
            return self.unit_price
        if self.discount:
            total = (self.discount * self.unit_price) / 100
            return int(self.unit_price - total)
        return self.total_price


class Comment(models.Model):
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    is_reply = models.BooleanField(default=False)
    reply = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='comment_reply')
    rate = models.PositiveIntegerField(default=1)
    create = models.DateTimeField(auto_now_add=True)
    comment_like = models.ManyToManyField(User, blank=True, related_name='com_like')
    total_like = models.PositiveIntegerField(default=0)

    def total_like(self):
        return self.comment_like.count()

    def __str__(self):
        return self.product.name


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'rate']


class ReplyForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


class Image(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='image_product')
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='image/', blank=True)


class Brand(models.Model):
    brand = models.CharField(max_length=200)

    def __str__(self):
        return self.brand


class Chart(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    unit_price = models.IntegerField(default=0)
    update = models.DateTimeField(auto_now=True)
    size = models.CharField(max_length=200, null=True, blank=True)
    color = models.CharField(max_length=200, null=True, blank=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='up_product', blank=True, null=True)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, related_name='var_product', blank=True, null=True)

    def __str__(self):
        return self.name


class View (models.Model):
    ip = models.CharField(max_length=200, blank=True, null=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='product')

    def __str__(self):
        return self.product.name


def product_post_saved(sender, instance, created, *args, **kwargs):
    data = instance
    if data.change == True:
        Chart.objects.create(product=data, unit_price=data.unit_price, update=data.update,
                             name=data.name)


post_save.connect(product_post_saved, sender=Products)
