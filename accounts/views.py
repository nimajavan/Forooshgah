from django.shortcuts import render, redirect, reverse
from .forms import *
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from kavenegar import *
from random import randint
from django.http import HttpResponse
from django.core.mail import EmailMessage
from django.views import View
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy


class EmailToken(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (text_type(user.is_active) + text_type(user.id) + text_type(timestamp))


email_generations = EmailToken()


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(username=data['user_name'], email=data['email'], password=data['password_1']
                                            , first_name=data['first_name'], last_name=data['last_name'])
            user.is_active = False
            user.save()
            domain = get_current_site(request).domain
            uidb64 = urlsafe_base64_encode(force_str(user.id))
            url = reverse('accounts:active', kwargs={'uidb64': uidb64, 'token': email_generations.make_token(user)})
            link = 'http://' + domain + url
            email = EmailMessage(
                'active user',
                link,
                'hi user',
                'test<nimajavangt@gmail.com>',
                [data['email']]
            )
            email.send(fail_silently=False)
            return redirect('home:products')
    else:
        form = UserRegisterForm()
    context = {'form': form}
    return render(request, 'accounts/register.html', context)


class RegisterEmail(View):
    def get(self, request, uidb64, token):
        user_id = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=user_id)
        if user and email_generations.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('accounts:login')


def login_user(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                user = authenticate(request, username=User.objects.get(email=data['username']),
                                    password=data['password'])
            except:
                user = authenticate(request, username=data['username'], password=data['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'login successful')
                return redirect('home:products')
    else:
        form = UserLoginForm

    return render(request, 'accounts/login.html', {'form': form})


def logout_user(request):
    logout(request)
    messages.success(request, 'logout successful')
    return redirect('home:products')


@login_required(login_url='accounts:login')
def user_profile(request):
    profile_ = Profile.objects.get(user_id=request.user.id)
    return render(request, 'accounts/profile.html', {'profile': profile_})


@login_required(login_url='accounts:login')
def user_update(request):
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateUserModelForm(request.POST, request.POST, instance=request.user.profile)
        if form and profile_form.is_valid():
            form.save()
            profile_form.save()
            messages.success(request, 'update successfully', 'success')
    else:
        form = UpdateUserForm(instance=request.user)
        profile_form = UpdateUserModelForm(instance=request.user.profile)
    context = {'form': form, 'profile_form': profile_form}
    return render(request, 'accounts/update.html', context)


@login_required(login_url='accounts:login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST, request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'successfully', 'success')
        else:
            messages.error(request, 'wrong password', 'danger')
    else:
        form = PasswordChangeForm(request.user)
    context = {'form': form}
    return render(request, 'accounts/password.html', context)


def login_phone(request):
    if request.method == 'POST':
        form = PhoneForm(request.POST)
        if form.is_valid():
            global phone, random_code
            phone = f"0{form.cleaned_data['phone']}"
            random_code = randint(100, 1000)
            api = KavenegarAPI(
                '77634E51555442727237775751353472616B6C61306F5037565169563431326B79697A50434C785A5473413D')
            params = {'sender': '100047778', 'receptor': phone, 'message': random_code}
            response = api.sms_send(params)
            HttpResponse(request, response)
            return redirect('accounts:verify_sms')
    else:
        form = PhoneForm()
    context = {'form': form}
    return render(request, 'accounts/login_phone.html', context)


def verify_sms(request):
    if request.method == 'POST':
        form = VerifyForm()
        if form.is_valid():
            if random_code == form.cleaned_data['code']:
                profile = Profile.objects.get(phone=phone)
                user = User.objects.get(profile__id=profile.id)
                login(request, user)
                messages.success(request, 'you are login successful')
                return redirect('accounts:profile')
            else:
                messages.error(request, 'code is wrong')
    else:
        form = VerifyForm()
    context = {'form': form}
    return render(request, 'accounts/verify_sms.html', context)


class ResetPassword(auth_views.PasswordResetView):
    template_name = 'accounts/reset.html'
    success_url = reverse_lazy('accounts:reset_done')
    email_template_name = 'accounts/link.html'


class DonePassword(auth_views.PasswordResetDoneView):
    template_name = 'accounts/done.html'


class ConfirmPassword(auth_views.PasswordResetConfirmView):
    template_name = 'accounts/confirm.html'
    success_url = reverse_lazy('accounts:complete')


class Complete(auth_views.PasswordResetCompleteView):
    template_name = 'accounts/complete.html'
