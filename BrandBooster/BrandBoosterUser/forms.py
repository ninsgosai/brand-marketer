from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Account
from django.contrib.auth import authenticate
from django.contrib.auth.views import *
from phonenumber_field.modelfields import PhoneNumberField

class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=60,widget=forms.TextInput(attrs={'placeholder':'firstname','class':'form-control','style':'height:55px;border-radius:0px;'}))
    last_name = forms.CharField(max_length=60,widget=forms.TextInput(attrs={'placeholder':'lastname','class':'form-control','style':'height:55px;border-radius:0px;'}))
    email = forms.EmailField(max_length=60,widget=forms.TextInput(attrs={'placeholder':'email','class':'form-control','style':'height:55px;border-radius:0px;'}))
    mobile_number = forms.CharField(max_length=60,widget=forms.TextInput(attrs={'placeholder':'mobile number','class':'form-control','style':'height:55px;border-radius:0px;',}))
    password1 = forms.CharField(label='password',widget=forms.PasswordInput(attrs={'placeholder':'password','class':'form-control','style':'background-color:white;height:55px;border-radius:0px;'}))
    password2 = forms.CharField(label='password',widget=forms.PasswordInput(attrs={'placeholder':'confirm password','class':'form-control','style':'background-color:white;height:55px;border-radius:0px;'}))
    class Meta:
        model = Account
        fields = ("first_name","last_name","email","mobile_number","password1","password2")
    
class ChangePasswordOtpForm(UserCreationForm):
    password1 = forms.CharField(label='password',widget=forms.PasswordInput(attrs={'placeholder':'password','class':'form-control','style':'background-color:white;height:55px;border-radius:0px;'}))
    password2 = forms.CharField(label='password',widget=forms.PasswordInput(attrs={'placeholder':'confirm password','class':'form-control','style':'background-color:white;height:55px;border-radius:0px;'}))
    class Meta:
        model = Account
        fields = ("password1","password2")


class AccountAuthenticationForm(forms.ModelForm):
    email = forms.EmailField(max_length=60,widget=forms.TextInput(attrs={'placeholder':'email','class':'form-control','style':'height:55px;border-radius:0px;'}))
    password = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'placeholder':'password','class':'form-control','style':'background-color:white;height:55px;border-radius:0px;'}))
    class Meta:
        model = Account
        fields = ('email','password')

    def clean(self):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        if not authenticate(email=email,password=password):
            raise forms.ValidationError("Invalid login")

# class auth_views(forms.ModelForm):
#     class Meta:
#         model = PasswordResetView
#         fields = ('email')

#class auth_views(PasswordResetView):
#    email = forms.EmailField(max_length=60,widget=forms.TextInput(attrs={'placeholder': 'username', 'class': 'form-control'}))