from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/', views.user_profile, name='profile'),
    path('update/', views.user_update, name='user_update'),
    path('ch_password/', views.change_password, name='change_password'),
    path('login_phone/', views.login_phone, name='login_phone'),
    path('verify_sms/', views.verify_sms, name='verify_sms'),
    path('active/', views.RegisterEmail.as_view(), name='active'),
    path('reset/', views.ResetPassword.as_view(), name='reset'),
    path('reset/done', views.DonePassword.as_view(), name='reset_done'),
    path('confirm/<uidb64>/<token>/', views.ConfirmPassword.as_view(), name='password_reset_done'),
    path('confrim/done/', views.Complete.as_view(), name='complete'),
]

