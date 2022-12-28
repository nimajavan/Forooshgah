from django.contrib import admin
from .models import *


class ProductVariantInline(admin.TabularInline):
    model = Variant


class ImageInline(admin.TabularInline):
    model = Image
    extra = 2


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'create', 'update', 'sub_category')
    prepopulated_fields = {
        'slug': ('name',)
    }


class SizeAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']


class VariantAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']


class ColorAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']


class ProductsAdmin(admin.ModelAdmin):
    list_display = (
    'name', 'create', 'update', 'amount', 'available', 'unit_price', 'discount', 'total_price', 'total_like')
    list_filter = ('available',)
    list_editable = ('amount',)
    raw_id_fields = ('category',)
    inlines = [ProductVariantInline, ImageInline]


class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'create', 'rate']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Products, ProductsAdmin)
admin.site.register(Variant, VariantAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Image)
admin.site.register(Brand)
admin.site.register(View)
