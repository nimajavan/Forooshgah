from django import forms
from django.contrib.auth.models import User
from .models import *


class UserRegisterForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    user_name = forms.CharField(max_length=50)
    email = forms.EmailField()
    password_1 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'placeholder': 'enter password'}))
    password_2 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'placeholder': 'repeat your password'}
                                                                           ))

    def clean_user_name(self):
        user = self.cleaned_data['user_name']
        if User.objects.filter(username=user).exists():
            raise forms.ValidationError('this username is exist')
        return user

    def clean_email(self):
        email_ = self.cleaned_data['email']
        if User.objects.filter(email=email_).exists():
            raise forms.ValidationError('this email is exist')
        return email_

    def clean_password_2(self):
        password_ = self.cleaned_data['password_1']
        password__ = self.cleaned_data['password_2']
        if password_ != password__:
            raise forms.ValidationError('password dose not match')
        elif len(password__) < 8:
            raise forms.ValidationError('password is too short')
        elif not any(x.isupper() for x in password__):
            raise forms.ValidationError('please insert one uppercase')
        else:
            return password_


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'password'}))


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class UpdateUserModelForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'address', 'image']


class PhoneForm(forms.Form):
    phone = forms.IntegerField()


class VerifyForm(forms.Form):
    code = forms.IntegerField()
