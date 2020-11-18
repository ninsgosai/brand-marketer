from django.contrib import admin

# Register your models here.

from .models import Review
from .models import Likes

admin.site.register(Review)
admin.site.register(Likes)