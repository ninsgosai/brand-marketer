from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *
import sys
from django.core import exceptions
import django.contrib.auth.password_validation as validators

class Account_Serial(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'

class Account_Update_Serial(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['first_name','last_name','mobile_number','mobile_code','profile_photo']

class Change_Password_serial(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['password']
    def validate_password(self, data):
        validators.validate_password(password=data, user=User)
        return data