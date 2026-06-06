from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import UserProfile


class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length=50, label='نام')
    last_name = forms.CharField(max_length=50, label='نام خانوادگی')
    username = forms.CharField(max_length=150, label='نام کاربری')
    email = forms.EmailField(label='ایمیل')
    phone = forms.CharField(max_length=20, label='تلفن همراه')
    password = forms.CharField(widget=forms.PasswordInput, label='رمز عبور')
    password2 = forms.CharField(widget=forms.PasswordInput, label='تکرار رمز عبور')

    def clean_username(self):
        u = self.cleaned_data['username']
        if User.objects.filter(username=u).exists():
            raise forms.ValidationError('این نام کاربری قبلاً ثبت شده است.')
        return u

    def clean_email(self):
        e = self.cleaned_data['email']
        if User.objects.filter(email=e).exists():
            raise forms.ValidationError('این ایمیل قبلاً ثبت شده است.')
        return e

    def clean(self):
        cd = super().clean()
        if cd.get('password') != cd.get('password2'):
            raise forms.ValidationError('رمز عبور و تکرار آن یکسان نیستند.')
        return cd


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, label='نام کاربری یا ایمیل')
    password = forms.CharField(widget=forms.PasswordInput, label='رمز عبور')
    remember = forms.BooleanField(required=False, label='مرا به خاطر بسپار')


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, required=False, label='نام')
    last_name = forms.CharField(max_length=50, required=False, label='نام خانوادگی')
    email = forms.EmailField(required=False, label='ایمیل')

    class Meta:
        model = UserProfile
        fields = ['phone', 'avatar', 'bio', 'company', 'city']
        labels = {
            'phone': 'تلفن همراه',
            'avatar': 'تصویر پروفایل',
            'bio': 'معرفی کوتاه',
            'company': 'شرکت / سازمان',
            'city': 'شهر',
        }

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email
