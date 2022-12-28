from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('category/<slug>/<int:id>/', views.products, name='category'),
    path('details/<int:id>/', views.products_details, name='products_details'),
    path('like/<int:id>', views.product_like, name='product_like'),
    path('unlike/<int:id>', views.product_unlike, name='product_unlike'),
    path('comment/<int:id>', views.comment, name='comment'),
    path('reply/<int:id>/<int:text_id>', views.comment_reply, name='comment_reply'),
    path('comment_like/<int:id>', views.comment_likes, name='comments_likes'),
    path('search/', views.product_search, name='product_search'),
    path('contact_us/', views.contact_us, name='contact_us'),
]
