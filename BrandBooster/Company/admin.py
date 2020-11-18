from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Category)
admin.site.register(Company_Info)
admin.site.register(Company_Marketing_Photos)
admin.site.register(Company_videos)
admin.site.register(Company_Audio)
admin.site.register(Company_Product_Photos)
admin.site.register(Main_Slider)