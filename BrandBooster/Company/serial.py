from rest_framework import serializers

from .models import *

class Category_Serial(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class Company_Info_Serial(serializers.ModelSerializer):
    class Meta:
        model = Company_Info
        fields = '__all__'

class Company_Update_Serial(serializers.ModelSerializer):
    class Meta:
        model = Company_Info
        fields = ['user_id','company_name','company_category','company_whatsapp','company_whatsapp_code','company_phone_code','company_short_info','company_long_info','company_ceo','company_address','company_state','company_city','company_pincode','company_phone','company_telephone','company_email','company_domain','company_status']

class Company_Marketing_Photos_Serial(serializers.ModelSerializer):
    class Meta:
        model = Company_Marketing_Photos
        fields = '__all__'

class Company_videos_Serial(serializers.ModelSerializer):
    class Meta:
        model = Company_videos
        fields = '__all__'

class Company_Product_Photos_Serial(serializers.ModelSerializer):
    class Meta:
        model = Company_Product_Photos
        fields = '__all__'

class Company_Audio_Serial(serializers.ModelSerializer):
    class Meta:
        model = Company_Audio
        fields = '__all__'

class Company_Info_View_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Company_Info
        fields = ['company_id','slug', 'company_name', 'company_short_info', 'company_photo','company_city']