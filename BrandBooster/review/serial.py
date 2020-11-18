from rest_framework import serializers

from .models import *


class Review_Serial(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class Review_Update_Serial(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['review','star']
