from django.shortcuts import redirect
from django.contrib.auth import *
from .models import *
from review.models import *
from django.contrib import messages

def is_login(my_function):
    def wrapper(request, *args, **kwargs):
        if request.user and request.user.is_authenticated:
            return my_function(request, *args, **kwargs)
        else:
            messages.error(request, 'You are not logged in. Please login.')
            return redirect('/')
    return wrapper

def feature_exist(my_function):
    def wrapper(request, *args, **kwargs):
        if 'slug' in kwargs:
            if Company_Info.objects.filter(slug=kwargs['slug']).exists():
                return my_function(request, *args, **kwargs)
            else:
                messages.error(request, 'Company does not exist.')
                return redirect('/')
        elif 'company_id' in kwargs:
            if Company_Info.objects.filter(company_id=kwargs['company_id']).exists():
                return my_function(request, *args, **kwargs)
            else:
                messages.error(request, 'Company does not exist.')
                return redirect('/')
        elif 'product_photo_id' in kwargs:
            if Company_Product_Photos.objects.filter(company_product_photos_id=kwargs['product_photo_id']).exists():
                return my_function(request, *args, **kwargs)
            else:
                messages.error(request, 'Product photo does not exist.')
                return redirect('/')
        elif 'marketing_photo_id' in kwargs:
            if Company_Marketing_Photos.objects.filter(company_Marketing_Photos_id=kwargs['marketing_photo_id']).exists():
                return my_function(request, *args, **kwargs)
            else:
                messages.error(request, 'Marketing photo does not exist.')
                return redirect('/')
        elif 'video_id' in kwargs:
            if Company_videos.objects.filter(company_videos_id=kwargs['video_id']).exists():
                return my_function(request, *args, **kwargs)
            else:
                messages.error(request, 'Video does not exist.')
                return redirect('/')
        elif 'audio_id' in kwargs:
            if Company_Audio.objects.filter(pk=kwargs['audio_id']).exists():
                return my_function(request, *args, **kwargs)
            else:
                messages.error(request, 'Audio does not exist.')
                return redirect('/')
        elif 'review_id' in kwargs:
            if Review.objects.filter(review_id=kwargs['review_id']).exists():
                return my_function(request, *args, **kwargs)
            else:
                messages.error(request,"Review does not exist.")
                return redirect('/')
    return wrapper

def is_authorized(my_function):
    def wrapper(request, *args, **kwargs):
        if 'company_id' in kwargs:
            company = Company_Info.objects.get(pk=kwargs['company_id'])
            if request.user.user_id == company.user_id.user_id:
                return my_function(request, *args, **kwargs)
            else:
                messages.error(request, 'You are not authorised.')
                return redirect('/')
        elif 'slug' in kwargs:
            company = Company_Info.objects.get(slug=kwargs['slug'])
            if request.user.user_id == company.user_id.user_id:
                return my_function(request, *args, **kwargs)
            else:
                messages.error(request, 'You are not authorised.')
                return redirect('/')
        elif 'review_id' in kwargs:
            review = Review.objects.get(review_id=kwargs['review_id'])
            if request.user.user_id == review.user_id.user_id:
                return my_function(request, *args, **kwargs)
            else:
                messages.error(request, 'You are not authorised.')
                return redirect('/')
        elif 'audio_id' in kwargs:
            feature = Company_Audio.objects.get(pk=kwargs['audio_id'])
            if request.user.user_id == feature.company.user_id.user_id:
                return my_function(request, *args, **kwargs)
            else:
                messages.error(request, 'You are not authorised.')
                return redirect('/')

        elif 'product_photo_id' in kwargs:
            feature = Company_Product_Photos.objects.get(company_product_photos_id=kwargs['product_photo_id'])
        elif 'marketing_photo_id' in kwargs:
            feature = Company_Marketing_Photos.objects.get(company_Marketing_Photos_id=kwargs['marketing_photo_id'])
        elif 'video_id' in kwargs:
            feature = Company_videos.objects.get(company_videos_id=kwargs['video_id'])
        elif 'audio_id' in kwargs:
            feature = Company_Audio.objects.get(pk=kwargs['audio_id'])
        
        if request.user.user_id == feature.company_id.user_id.user_id:
            return my_function(request, *args, **kwargs)
        else:
            messages.error(request, 'You are not authorised.')
            return redirect('/')
    return wrapper

def is_unauthorized(my_function):
    def wrapper(request, *args, **kwargs):
        if 'company_id' in kwargs:
            company = Company_Info.objects.get(pk=kwargs['company_id'])
            if request.user.user_id != company.user_id.user_id:
                return my_function(request, *args, **kwargs)
            else:
                messages.error(request, 'You are not authorised.')
                return redirect('/')
        # elif 'reviewid' in request.POST:
        #     review = Review.objects.get(review_id=request.POST['reviewid'])
        #     if request.user.user_id == review.user_id.user_id:
        #         return my_function(request, *args, **kwargs)
        #     else:
        #         messages.error(request, 'You are not authorised.')
        #         return redirect('/')
        # if 'product_photo_id' in kwargs:
        #     feature = Company_Product_Photos.objects.get(company_product_photos_id=kwargs['product_photo_id'])
        # if 'marketing_photo_id' in kwargs:
        #     feature = Company_Marketing_Photos.objects.get(company_Marketing_Photos_id=kwargs['marketing_photo_id'])
        # if 'video_id' in kwargs:
        #     feature = Company_videos.objects.get(company_videos_id=kwargs['video_id'])
        
        # if request.user.user_id == feature.company_id.user_id.user_id:
        #     return my_function(request, *args, **kwargs)
        # else:
        #     messages.error(request, 'You are not authorised.')
        #     return redirect('/')
    return wrapper