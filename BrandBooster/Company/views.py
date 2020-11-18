from django.shortcuts import render,redirect,reverse
from BrandBoosterUser.models import Account
from social_django.models import * 
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from BrandBoosterUser.forms import RegistrationForm, AccountAuthenticationForm
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from review.models import *
from .decorators import *
from .models import *
from .serial import *
from .forms import *
from brandbooster.utils import send_email_for_user_account_activation
import datetime
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import pytube
import random
from allauth.socialaccount.models import SocialApp, SocialAccount


@api_view(['POST'])
def List_Category(request):
    serializer = Category_Serial(Category.objects.all(), many=True)
    return Response({"error": 0, "data": serializer.data})

@api_view(['POST'])
def List_Company_By_Category(request):
    try:
        category = Category.objects.get(name=request.POST['categoryname'])
    except Category.DoesNotExist:
        return Response({"error": 1, "data": [], "message": "Category does not exist."})
    companies = Company_Info.objects.filter(company_status=True, company_category=category)
    serializer = Company_Info_View_Serializer(companies, many=True)
    return Response({"error": 0, "data" : serializer.data})

@api_view(['GET', 'POST'])
def User_Company_List(request,user_id):
    Company_Info_Tasks = Company_Info.objects.filter(user_id=user_id).order_by('?')
    if Company_Info_Tasks:    
        Company_Info_Serializer = Company_Info_Serial(Company_Info_Tasks, many=True)
        return Response({"error": 0, "data": Company_Info_Serializer.data})
    else:
        return Response({"error": 1, "data": [], "message": "Company not available."})

@api_view(['GET', 'POST'])
def Company_Info_Detailed(request,pk):
    Company_Info_Tasks = Company_Info.objects.filter(slug=pk)
    if Company_Info_Tasks:    
        Company_Info_Serializer = Company_Info_Serial(Company_Info_Tasks[0], many=False)
        category_id = Company_Info_Serializer.data['company_category']
        category_name = Category.objects.filter(id=category_id)
        contax = {
            'company_id': Company_Info_Serializer.data['company_id'],
            'company_name': Company_Info_Serializer.data['company_name'],
            'slug' : Company_Info_Serializer.data['slug'],
            'custom_category': Company_Info_Serializer.data['custom_category'],
            'company_short_info': Company_Info_Serializer.data['company_short_info'],
            'company_long_info': Company_Info_Serializer.data['company_long_info'],
            'company_ceo': Company_Info_Serializer.data['company_ceo'],
            'company_address': Company_Info_Serializer.data['company_address'],
            'company_state': Company_Info_Serializer.data['company_state'],
            'company_city': Company_Info_Serializer.data['company_city'],
            'company_pincode': Company_Info_Serializer.data['company_pincode'],
            'company_phone': Company_Info_Serializer.data['company_phone'],
            'company_whatsapp': Company_Info_Serializer.data['company_whatsapp'],   
            'company_whatsapp_code': Company_Info_Serializer.data['company_whatsapp_code'],   
            'company_phone_code': Company_Info_Serializer.data['company_phone_code'],   
            'company_telephone': Company_Info_Serializer.data['company_telephone'],
            'company_email': Company_Info_Serializer.data['company_email'],
            'company_domain': Company_Info_Serializer.data['company_domain'],
            'company_status': Company_Info_Serializer.data['company_status'],
            'company_photo': Company_Info_Serializer.data['company_photo'],
            'cover_image': Company_Info_Serializer.data['cover_image'],
            'date_time_created': Company_Info_Serializer.data['date_time_created'],
            'date_time_modified': Company_Info_Serializer.data['date_time_modified'],
            'user_id': Company_Info_Serializer.data['user_id'],
            'company_category': Company_Info_Serializer.data['company_category'],
            'company_category_name': category_name[0].name
        }
        return Response({"error": 0, "data": contax})
    else:
        return Response({"error": 1, "data": [], "message": "Company not available."})


@api_view(['POST'])
def Company_Info_View(request):
    companies = Company_Info.objects.filter(company_status=True).order_by('?')
    if companies:
        page = request.POST['pk']
        if page == '1':
            companies = Company_Info.objects.filter(company_status=True).order_by('?')
        else: 
            companies = Company_Info.objects.filter(company_status=True)
        paginator = Paginator(companies, 5)
        try:
            company = paginator.page(page)
        except PageNotAnInteger:
            company = paginator.page(1)
        except EmptyPage:
            company = paginator.page(paginator.num_pages)
            
        serializer_context = {'request': request}

        serializer = Company_Info_View_Serializer(company, many=True)
        if int(request.POST['pk']) > paginator.num_pages or int(request.POST['pk'])<=0:
            return Response({"error": 0, "data" : {},'total_page':paginator.num_pages,'current_page':page})
        else:
            return Response({"error": 0, "data" : serializer.data,'total_page':paginator.num_pages,'current_page':page})
    else:
        return Response({"error": 1, "data": [], "message": "No company available."})


@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def Company_Info_Create(request):
    try:
        account = Account.objects.get(user_id=request.data['user_id'])
    except Account.DoesNotExist:
        return Response({"error": 1, "data": [], "message": "User does not exist."})
    
    serializer = Company_Info_Serial(data=request.data)
    if serializer.is_valid():
        company = serializer.save()
        company.company_status = True
        
        if 'custom_category' in request.POST and request.POST["custom_category"] != "":
            custom_category = request.POST['custom_category']

            # CREATE A NEW CATEGORY
            if not Category.objects.filter(name=custom_category).exists():
                category = Category()
                category.name = custom_category
                category.save()
    
            # GET THE EXISTING CATEGORY
            else:
                category = Category.objects.get(name=custom_category)
            
            # SET COMPANY CATEGORY TYPE
            company.company_category = category
            company.custom_category = ""
            
        company.save()
        # serializer = Company_Info_Serial(instance=company)
        
        return Response({"error": 0, "data": serializer.data})

    if 'company_name' in serializer.errors:
        return Response({"error": 2, "data": [], "message": "Company name may not be blank."})
    if 'company_short_info' in serializer.errors:
        return Response({"error": 3, "data": [], "message": "Company short info name may not be blank."})
    if 'company_long_info' in serializer.errors:
        return Response({"error": 4, "data": [], "message": "Company long info name may not be blank."})
    if 'company_ceo' in serializer.errors:
        return Response({"error": 5, "data": [], "message": "Company CEO name may not be blank."})
    if 'company_phone' in serializer.errors:
        if serializer.errors['company_phone'][0].code == 'blank':
            return Response({"error": 6, "data": [], "message": "Company phone number may not be blank."})
        if serializer.errors['company_phone'][0].code == "invalid_phone_number":
            return Response({"error": 7, "data": [], "message": "The phone number entered is not valid."})
        if serializer.errors['company_phone'][0].code == "unique":
            return Response({"error": 8, "data": [], "message": "Company with this phone number already exist."})
    if 'company_whatsapp' in serializer.errors:
        if serializer.errors['company_whatsapp'][0].code == 'blank':
            return Response({"error": 25, "data": [], "message": "Company whatsapp number may not be blank."})
        if serializer.errors['company_whatsapp'][0].code == "invalid_phone_number":
            return Response({"error": 26, "data": [], "message": "The whatsapp number entered is not valid."})
        if serializer.errors['company_whatsapp'][0].code == "unique":
            return Response({"error": 27, "data": [], "message": "Company with this whatsapp phone number already exist."})
    if 'company_email' in serializer.errors:
        if serializer.errors['company_email'][0].code == "blank":
            return Response({"error": 9, "data": [], "message": "Company email may not be blank."})
        if serializer.errors['company_email'][0].code == "invalid":
            return Response({"error": 10, "data": [], "message": "The email entered is not valid."})
        if serializer.errors['company_email'][0].code == "unique":
            return Response({"error": 11, "data": [], "message": "Company with this email already exist."})
    if 'company_domain' in  serializer.errors:
        if serializer.errors['company_domain'][0].code == "blank":
            return Response({"error": 12, "data": [], "message": "Company domain may not be blank."})
        if serializer.errors['company_domain'][0].code == "unique":
            return Response({"error": 13, "data": [], "message": "Company with this domain already exist."})
    if 'company_category' in serializer.errors:
        if serializer.errors['company_category'][0].code == "does_not_exist":
            return Response({"error": 14, "data": [], "message": "Category does not exist."})
    if 'company_address' in serializer.errors:
        if serializer.errors['company_address'][0].code == "blank":
            return Response({"error": 15, "data": [], "message": "Address may not be blank."})
    if 'company_city' in serializer.errors:
        if serializer.errors['company_city'][0].code == "blank":
            return Response({"error": 16, "data": [], "message": "City may not be blank."})
    if 'company_state' in serializer.errors:
        if serializer.errors['company_state'][0].code == "blank":
            return Response({"error": 17, "data": [], "message": "State may not be blank."})
    if 'company_pincode' in serializer.errors:
        if serializer.errors['company_pincode'][0].code == "invalid":
            return Response({"error": 18, "data": [], "message": "Pincode may not be blank."})
        if serializer.errors['company_pincode'][0].code == "max_value":
            return Response({"error": 19, "data": [], "message": "Pincode is invalid."})
    if 'company_photo' in serializer.errors:
        if serializer.errors['company_photo'][0].code == "invalid":
            return Response({"error": 20, "data": [], "message": "Company photo may not be blank."})
        if serializer.errors['company_photo'][0].code == "invalid_image":
            return Response({"error": 21, "data": [], "message": "Company photo should be in valid image format."})
    if 'cover_image' in serializer.errors:
        if serializer.errors['cover_image'][0].code == "invalid":
            return Response({"error": 22, "data": [], "message": "Cover photo may not be blank."})
        if serializer.errors['cover_image'][0].code == "invalid_image":
            return Response({"error": 23, "data": [], "message": "Cover photo should be in valid image format."})

    return Response({"error": 24, "data": [], "message": "Data is incorrect"})


@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def Company_Info_Update(request, pk):
    try:
        account = Account.objects.get(user_id=request.data['user_id'])
    except Account.DoesNotExist:
        return Response({"error": 1, "data": [], "message": "User does not exist."})
    try:
        company = Company_Info.objects.get(company_id=pk)
    except Company_Info.DoesNotExist:
        return Response({"error": 2, "data": [], "message": "Company does not exist."})
    
    if company.user_id.user_id != account.user_id:
        return Response({"error": 3, "data": [], "message": "You don't have access to this company."})
    
    serializer = Company_Update_Serial(instance=company, data=request.data)
    if serializer.is_valid():
        company_photo, cover_image = False, False
        if 'company_photo' in request.FILES:
            if 'image' in request.FILES['company_photo'].content_type:
                company_photo = True
            else:
                return Response({"error": 22, "data": [], "message": "Company photo should be in valid image format."})

        if 'cover_image' in request.FILES:
            if 'image' in request.FILES['cover_image'].content_type:
                cover_image = True
            else:
                return Response({"error": 23, "data": [], "message": "Cover photo should be in valid image format."})
        company = serializer.save()

        company.company_status = True

        if company_photo: company.company_photo = request.FILES['company_photo']
        if cover_image: company.cover_image = request.FILES['cover_image']

        if 'custom_category' in request.POST and request.POST["custom_category"] != "":
            custom_category = request.POST['custom_category']

            # CREATE A NEW CATEGORY
            if not Category.objects.filter(name=custom_category).exists():
                category = Category()
                category.name = custom_category
                category.save()
    
            # GET THE EXISTING CATEGORY
            else:
                category = Category.objects.get(name=custom_category)
            
            # SET COMPANY CATEGORY TYPE
            company.company_category = category
            company.custom_category = ""
            
        company.save()
        
        serializer = Company_Info_Serial(instance=company)
        return Response({"error": 0, "data": serializer.data})

    if 'company_name' in serializer.errors:
        return Response({"error": 4, "data": [], "message": "Company name may not be blank."})
    if 'company_short_info' in serializer.errors:
        return Response({"error": 5, "data": [], "message": "Company short info name may not be blank."})
    if 'company_long_info' in serializer.errors:
        return Response({"error": 6, "data": [], "message": "Company long info name may not be blank."})
    if 'company_ceo' in serializer.errors:
        return Response({"error": 7, "data": [], "message": "Company CEO name may not be blank."})
    if 'company_phone' in serializer.errors:
        if serializer.errors['company_phone'][0].code == 'blank':
            return Response({"error": 8, "data": [], "message": "Company phone number may not be blank."})
        if serializer.errors['company_phone'][0].code == "invalid_phone_number":
            return Response({"error": 9, "data": [], "message": "The phone number entered is not valid."})
        if serializer.errors['company_phone'][0].code == "unique":
            return Response({"error": 10, "data": [], "message": "Company with this phone number already exist."})
    if 'company_whatsapp' in serializer.errors:
        if serializer.errors['company_whatsapp'][0].code == 'blank':
            return Response({"error": 8, "data": [], "message": "Company whatsapp number may not be blank."})
        if serializer.errors['company_whatsapp'][0].code == "invalid_phone_number":
            return Response({"error": 9, "data": [], "message": "The whatsapp number entered is not valid."})
        if serializer.errors['company_whatsapp'][0].code == "unique":
            return Response({"error": 10, "data": [], "message": "Company with this whatsapp number already exist."})
    if 'company_email' in serializer.errors:
        if serializer.errors['company_email'][0].code == "blank":
            return Response({"error": 11, "data": [], "message": "Company email may not be blank."})
        if serializer.errors['company_email'][0].code == "invalid":
            return Response({"error": 12, "data": [], "message": "The email entered is not valid."})
        if serializer.errors['company_email'][0].code == "unique":
            return Response({"error": 13, "data": [], "message": "Company with this email already exist."})
    if 'company_domain' in  serializer.errors:
        if serializer.errors['company_domain'][0].code == "blank":
            return Response({"error": 14, "data": [], "message": "Company domain may not be blank."})
        if serializer.errors['company_domain'][0].code == "unique":
            return Response({"error": 15, "data": [], "message": "Company with this domain already exist."})
    if 'company_category' in serializer.errors:
        if serializer.errors['company_category'][0].code == "does_not_exist":
            return Response({"error": 16, "data": [], "message": "Category does not exist."})
    if 'company_address' in serializer.errors:
        if serializer.errors['company_address'][0].code == "blank":
            return Response({"error": 17, "data": [], "message": "Address may not be blank."})
    if 'company_city' in serializer.errors:
        if serializer.errors['company_city'][0].code == "blank":
            return Response({"error": 18, "data": [], "message": "City may not be blank."})
    if 'company_state' in serializer.errors:
        if serializer.errors['company_state'][0].code == "blank":
            return Response({"error": 19, "data": [], "message": "State may not be blank."})
    if 'company_pincode' in serializer.errors:
        if serializer.errors['company_pincode'][0].code == "invalid":
            return Response({"error": 20, "data": [], "message": "Pincode may not be blank."})
        if serializer.errors['company_pincode'][0].code == "max_value":
            return Response({"error": 21, "data": [], "message": "Pincode is invalid."})
            
    return Response({"error": 24, "data": [], "message": "Data is incorrect"})


@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def Company_Info_Delete(request, pk):
    try:
        company = Company_Info.objects.get(company_id=pk)
    except Company_Info.DoesNotExist:
        return Response({"error": 1, "data": [], "message": "Company does not exist."})

    company.delete()
    return Response({"error": 0, "data": [], "message": "Data Deleted."})


################################################################################################
#Company_Marketing_Photos
################################################################################################
@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def Company_Marketing_Photos_View(request,company_id):
    photos = Company_Marketing_Photos.objects.filter(company_id=company_id)
    if photos:
        serializer = Company_Marketing_Photos_Serial(photos, many=True)
        return Response({"error": 0, "data": serializer.data})
    else:
        return Response({"error": 1, "data": [], "message": "Company marketing photos does not exist."})



@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def Company_Marketing_Photos_Create(request):
    try:
        company = Company_Info.objects.get(company_id=request.data['company_id'])
    except Company_Info.DoesNotExist:
        return Response({"error": 1, "data": [], "message": "Company does not exist."})
    
    serializer = Company_Marketing_Photos_Serial(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"error": 0, "data": serializer.data})
    else:
        return Response({"error": 2, "data": [], "message": "Please fill all data."})


@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def Company_Marketing_Photos_Delete(request, pk):
    try:
        photo = Company_Marketing_Photos.objects.get(company_Marketing_Photos_id=pk)
    except Company_Marketing_Photos.DoesNotExist:
        return Response({"error": 1, "data": [], "message": "Company Marketing Photo does not exist."})
    
    photo.delete()
    return Response({"error": 0, "data": [], "message": "Data Deleted."})


################################################################################################
#Company_videos
################################################################################################
@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def Company_videos_View(request,company_id):
    videos = Company_videos.objects.filter(company_id=company_id)
    if videos:
        serializer = Company_videos_Serial(videos, many=True)
        return Response({"error": 0, "data": serializer.data})
    else:
        return Response({"error": 1, "data": [], "message": "Company videos does not exist."})


@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def Company_videos_Create(request):
    try:
        company = Company_Info.objects.get(company_id=request.data['company_id'])
    except Company_Info.DoesNotExist:
        return Response({"error": 1, "data": [], "message": "Company does not exist."})
    
    serializer = Company_videos_Serial(data=request.data)
    if serializer.is_valid():
        link = request.POST["video_link"]
        try:
            yt = pytube.YouTube(link)
            company_video = serializer.save()
            company_video.video_link = yt.video_id
            company_video.save()
            return Response({"error": 0, "data": serializer.data})
        except Exception as e:
            return Response({"error": 3, "data": [], "message": "Please Enter a valid youtube link."})
    else:
        return Response({"error": 2, "data": [], "message": "Please fill all data."})


@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def Company_videos_Delete(request, pk):
    try:
        video = Company_videos.objects.get(company_videos_id=pk)
    except Company_videos.DoesNotExist:
        return Response({"error": 1, "data": [], "message": "Video does not exist."})

    video.delete()
    return Response({"error": 0, "data": [], "message": "Data Deleted."})


################################################################################################
#Company_Product_Photos
################################################################################################
@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def Company_Product_Photos_View(request,company_id):
    photos = Company_Product_Photos.objects.filter(company_id=company_id)
    if photos:    
        serializer = Company_Product_Photos_Serial(photos, many=True)
        return Response({"error": 0, "data": serializer.data})
    else:
        return Response({"error": 1, "data": [], "message": "Product photos does not exist."})


@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def Company_Product_Photos_Create(request):
    try:
        company = Company_Info.objects.get(company_id=request.data['company_id'])
    except Company_Info.DoesNotExist:
        return Response({"error": 1, "data": [], "message": "Company does not exist."})

    serializer = Company_Product_Photos_Serial(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"error": 0, "data": serializer.data})
    else:
        return Response({"error": 2, "data": [], "message": "The submitted data was not a file. Check the encoding type on the form."})


@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def Company_Product_Photos_Delete(request, pk):
    try:
        photo = Company_Product_Photos.objects.get(company_product_photos_id=pk)
    except Company_Product_Photos.DoesNotExist:
        return Response({"error": 1, "data": [], "message": "Product Photo does not exist."})
    
    photo.delete()
    return Response({"error": 0, "data": [], "message": "Data Deleted."})


################################################################################################
#Company_audios
################################################################################################
@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def Company_Audio_View(request,company_id):
    audios = Company_Audio.objects.filter(company_id=company_id)
    if audios:
        serializer = Company_Audio_Serial(audios, many=True)
        return Response({"error": 0, "data": serializer.data})
    else:
        return Response({"error": 1, "data": [], "message": "Company audios does not exist."})


@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def Company_Audio_Create(request):
    try:
        account = Account.objects.get(user_id=request.data['user_id'])
    except Account.DoesNotExist:
        return Response({"error": 1, "data": [], "message": "User does not exist."})
    try:
        company = Company_Info.objects.get(company_id=request.data['company'])
    except Company_Info.DoesNotExist:
        return Response({"error": 2, "data": [], "message": "Company does not exist."})
    
    if company.user_id.user_id != account.user_id:
        return Response({"error": 3, "data": [], "message": "You don't have access to this company."})
    
    serializer = Company_Audio_Serial(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"error": 0, "data": serializer.data})
    else:
        return Response({"error": 4, "data": [], "message": "Please fill all data."})


@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def Company_Audio_Delete(request, audio_id):
    try:
        audio = Company_Audio.objects.get(pk=audio_id)
    except Company_Audio.DoesNotExist:
        return Response({"error": 1, "data": [], "message": "Audio does not exist."})

    audio.delete()
    return Response({"error": 0, "data": [], "message": "Data Deleted."})


####################################################################################################################################
#                                                            WEBSITE
####################################################################################################################################

def home(request):

    if request.user.is_authenticated:
        if SocialAccount.objects.filter(user=request.user.user_id).exists():
            social_user = SocialAccount.objects.get(user=request.user.user_id)
            if social_user.provider == "google" and Account.objects.filter(user_id=request.user.user_id).exists():
                userData = Account.objects.get(user_id=request.user.user_id)
                if userData.google_token == "":
                    userData.google_token = social_user.uid
                    userData.login_type = 2
                    userData.save() 
        if SocialAccount.objects.filter(user=request.user.user_id).exists():
            social_user = SocialAccount.objects.get(user=request.user.user_id)
            if social_user.provider == "facebook" and Account.objects.filter(user_id=request.user.user_id).exists():
                userData = Account.objects.get(user_id=request.user.user_id)
                if userData.facebook_token == "":
                    userData.facebook_token = social_user.uid
                    userData.login_type = 1
                    userData.save() 

    context = {}
    page = request.GET.get('page', 1)
    slider = Main_Slider.objects.all()

    if page == 1:
        company_list = Company_Info.objects.filter(company_status=True).order_by('?')
    else:
        company_list = Company_Info.objects.filter(
                        ~Q(company_id=company_list[0].company_id),
                        ~Q(company_id=company_list[1].company_id),
                        ~Q(company_id=company_list[2].company_id),
                        ~Q(company_id=company_list[3].company_id),
                        ~Q(company_id=company_list[4].company_id),
                        ~Q(company_id=company_list[5].company_id),
                        ~Q(company_id=company_list[6].company_id),
                        ~Q(company_id=company_list[7].company_id),
                        ~Q(company_id=company_list[8].company_id),
                        ~Q(company_id=company_list[9].company_id),
                        ~Q(company_id=company_list[10].company_id),
                        ~Q(company_id=company_list[11].company_id),
                        company_status=True,
                        )
    category = Category.objects.all()

    query = request.GET.get('company_name')
    query_filter = request.GET.get('company_category')
    if query:
        company_list = Company_Info.objects.filter(
            Q(company_name__iregex=query,company_status=True)|Q(company_city__iregex=query,company_status=True)
        )
    if query_filter and query_filter != "0":
        company_list = Company_Info.objects.filter(
            Q(company_category=int(query_filter),company_status=True)
        )

    company_paginator = Paginator(company_list, 12)
    try:                        companies = company_paginator.page(page)
    except PageNotAnInteger:    companies = company_paginator.page(1)
    except EmptyPage:           companies = company_paginator.page(paginator.num_pages)


    form_login = AccountAuthenticationForm()
    form_registration = RegistrationForm()
    
    if request.method == "POST":
        if request.POST['register'] =='r':
            form_registration = RegistrationForm(request.POST)
            if form_registration.is_valid():
                try:
                    user = form_registration.save(commit=False)
                    user.is_active = False
                    s =  str(datetime.datetime.now())
                    characters_to_remove = ":._- "
                    for character in characters_to_remove:
                        s = s.replace(character, "")
                    user.username =  s
                    email = form_registration.cleaned_data.get('email')
                    send_email_for_user_account_activation(s,email)
                    messages.success(request, f'your account has been created! check your email to activate your account.')
                    user.save()
                except:
                    messages.error(request, f'pleasefdf credentials are invalid')
            else: 
                messages.error(request, f'your credentials are invalid')
        else:
            form_login = AccountAuthenticationForm(request.POST)
            try:
                if form_login.is_valid():
                    email = request.POST['email']
                    password = request.POST['password']
                    user = authenticate(email=email,password=password)

                    if user:
                        if user.user_status == False:
                            messages.error(request, f'your account is disabled. please contact the administrator.')
                        else: 
                            login(request,user)
                            return redirect("/")
                else:
                    if Account.objects.filter(email=request.POST['email']).exists() and Account.objects.get(email=request.POST['email']).login_type != 0:
                        messages.error(request,'Your Acount is registered via social media. Please login from from your social media account only.')
                    else:
                        messages.error(request, f'your login credentials are invalid')
            except:
                pass
    
    context['forml'] = form_login
    context['form'] = form_registration
    context['companies'] = companies
    context['slider'] = slider
    context['category'] = category
    context['query'] = query
    if query_filter:
        context['query_filter'] = int(query_filter)
    context['forml'] = form_login
    return render(request, 'index.html', context)

@feature_exist
def products(request,slug):
    forml = AccountAuthenticationForm()
    form = RegistrationForm()
    context = {}

    # GET ALL COMPANY DATA
    # company = Company_Info.objects.get(company_id=company_id,company_status=True)
    company = Company_Info.objects.filter(slug=slug,company_status=True)
    if company.exists():
        company=company.first()
    else:
        return HttpResponse("No Company Found")
    products = Company_Product_Photos.objects.filter(company_id=company.pk)
    videos = Company_videos.objects.filter(company_id=company.pk)
    marketings = Company_Marketing_Photos.objects.filter(company_id=company.pk)
    audios = Company_Audio.objects.filter(company_id=company.pk)

    # CALCULATE AVERAGE STAR RATINGS
    reviews = Review.objects.filter(company_id=company.pk)
    review_count = reviews.count()
    sum = 0
    star_number = 0
    if review_count != 0:
        for i in reviews:
            if i.star:
                sum = sum + i.star
                star_number += 1
        sum = int(sum/star_number) if star_number else 0

    # RETRIVE ALL REVIEWS AND USER REVIEWS
    if request.user.is_authenticated:
        total_reviews = Review.objects.filter(~Q(user_id=request.user.user_id),company_id=company.pk)
        user_reviews = Review.objects.filter(user_id=request.user, company_id=company.pk)

        # CHECK IF USER HAS LIKED THIS COMPANY OR NOT
        user_liked = Likes.objects.filter(user_id=request.user,company_id=company.pk)
    else:
        total_reviews = Review.objects.filter(company_id=company.pk)
        user_reviews = []
        user_liked = {}

    if user_liked:
        user_liked = user_liked[0]
    else:
        user_liked = {'like': 0}

    context['company'] = company
    context['products'] = products    
    context['videos'] = videos
    context['marketings'] = marketings
    context['audios'] = audios
    context['user_liked'] = user_liked
    context['total_reviews'] = total_reviews
    context['user_reviews'] = user_reviews
    context['lst_index'] = [1,2,3,4,5]
    context['sum'] = sum
    context['forml'] = forml
    context['form'] = form

    return render(request, 'product.html', context)


@is_login
@feature_exist
@is_authorized
def edit_company(request, company_id):
    company = Company_Info.objects.get(pk=company_id)
    form = CompanyEditForm(instance=company)
    if request.method == "POST":
        form = CompanyEditForm(request.POST, request.FILES, instance=company)
        if form.is_valid():
            if company.company_phone:
                company.company_phone_code = company.company_phone.country_code
            if company.company_whatsapp:
                company.company_whatsapp_code = company.company_whatsapp.country_code

            if request.POST['custom_category'] and not Category.objects.filter(name=request.POST['custom_category']).exists():
                category = Category(name=request.POST['custom_category']).save()
                company=form.save()
                company.custom_category=""
                # company.slug = unique_slug_generator(company)
                company.company_category = category
                company.save()
            elif request.POST['custom_category'] and Category.objects.filter(name=request.POST['custom_category']).exists():
                category = Category.objects.get(name=request.POST['custom_category'])
                company=form.save()
                company.custom_category=""
                # company.slug = unique_slug_generator(company)
                company.company_category = category
                company.save()
            else:
                company=form.save()
                # company.slug = unique_slug_generator(company)
                company.save()
            messages.success(request, 'company updated successfully!')
            return redirect('/my_company/')
    return render(request,'my_company_edit.html', {'form': form,'company_id':company_id})

@is_login
def add_company(request):
    form = CompanyCreateForm()
    if request.method == "POST":
        form = CompanyCreateForm(request.POST, request.FILES)
        if form.is_valid():
            company = form.save(commit=False)
            company.user_id = request.user
            company.company_status = True
            if request.POST['custom_category'] and not Category.objects.filter(name=request.POST['custom_category']).exists():
                Category(name=request.POST['custom_category']).save()
                maxId = Category.objects.all().order_by("-id")[0]
                company.company_category = maxId
            elif request.POST['custom_category'] and Category.objects.filter(name=request.POST['custom_category']).exists():
                category = Category.objects.get(name=request.POST['custom_category'])
                company=form.save()
                company.custom_category=""
                company.company_category = category
                company.save()

            if company.company_phone:
                company.company_phone_code = company.company_phone.country_code
            if company.company_whatsapp:
                company.company_whatsapp_code = company.company_whatsapp.country_code
            company.save()
            messages.success(request, 'company created successfully!')
            return redirect('/my_company/')
    return render(request,'add_company.html', {'form': form})


def active(request, username):
    try:
        user = Account.objects.get(username=username)
    except Account.DoesNotExist:
        messages.warning(request, f'Account does not exists.')
        return redirect('/')

    if user.is_active == True :
        messages.warning(request, f'your account is already active.')
    else:
        user.is_active = True
        user.save()
        messages.success(request, f'your account is activated successfully! please login.')
    return redirect('/')

@is_login
def my_profile(request):
    return render(request,'my_profile.html')

@is_login
def edit_profile(request):
    if request.method == "GET":
        return render(request,'my_profile_edit.html')

    email = request.POST['email']
    if Account.objects.filter(~Q(pk=request.user.user_id), email=email):
        messages.add_message(request, messages.ERROR, 'This email is already exist!')
        return render(request,'my_profile_edit.html')
    
    mobilenumber = request.POST['mobile']

    # if len(mobilenumber) > 13 or len(mobilenumber) < 13:
    #     messages.add_message(request, messages.ERROR, 'Invalid mobile number!')
    #     return render(request,'my_profile_edit.html')

    if Account.objects.filter(~Q(pk=request.user.user_id), mobile_number=mobilenumber):
        messages.add_message(request, messages.ERROR, 'This mobile number is already exist!')
        return render(request,'my_profile_edit.html')

    companyuser = Account.objects.get(pk=request.user.user_id)
    if bool(request.FILES.get('profile_photo', False)) == True:
        companyuser.profile_photo = request.FILES['profile_photo']
    companyuser.first_name = request.POST['firstname']
    companyuser.last_name = request.POST['lastname']
    companyuser.email = email
    companyuser.mobile_number = mobilenumber
    if companyuser.mobile_number:
        companyuser.mobile_code = companyuser.mobile_number.country_code
    companyuser.save()
    messages.success(request,"Profile Edited Succesfully!")
    return redirect('my_profile')

@is_login
def my_company(request):
    page = request.GET.get('page', 1)
    paginator = Paginator(Company_Info.objects.filter(company_status=True, user_id=request.user.user_id).order_by('?'), 12)
    try:                        companies = paginator.page(page)
    except PageNotAnInteger:    companies = paginator.page(1)
    except EmptyPage:           companies = paginator.page(paginator.num_pages)
    return render(request, 'my_company.html', {'companies': companies})

@is_login
def change_password(request):
    pform = PasswordChangeForm(user=request.user)
    if request.method == 'POST':
        pform = PasswordChangeForm(user=request.user, data= request.POST)
        if pform.is_valid():
            pform.save()
            logout(request)
            messages.success(request, f'you have changed your password successfully! please login.')
            return redirect('/')
    return render(request, 'password_change.html',{'pform':pform})

@is_login
def logout_user(request):
    logout(request)
    return redirect('/')



@is_login
@feature_exist
@is_authorized
def add_product_photo(request, company_id):
    if request.method == "POST":
        if 'company_image' in request.FILES and 'image_name' in request.POST:
            Company_Product_Photos(
                image_name=request.POST['image_name'], 
                company_prd_image=request.FILES['company_image'],
                company_id_id=company_id).save()
            messages.success(request, 'photo uploaded successfully!')
        else:
            messages.error(request, 'please fill all data!')
    company_id =Company_Info.objects.get(company_id=company_id)
    return render(request, 'add_product_photo.html',{'company_id':company_id})

@is_login
@feature_exist
@is_authorized
def add_marketing_photo(request, company_id):
    if request.method == "POST":
        if 'company_image' in request.FILES and 'image_name' in request.POST:
            Company_Marketing_Photos(
                image_name=request.POST['image_name'],
                company_mrk_image=request.FILES['company_image'],
                company_id_id=company_id
            ).save()
            messages.success(request, 'photo uploaded successfully!')
        else:
            messages.error(request, 'please fill all data!')
    company_id =Company_Info.objects.get(company_id=company_id)
    return render(request, 'add_marketing_photo.html',{'company_id':company_id})

@is_login
@feature_exist
@is_authorized
def add_audio(request, company_id):
    if request.method == "POST":
        if 'audio_file' in request.FILES and 'audio_name' in request.POST:
            Company_Audio(
                company_id=company_id,
                audio_name=request.POST['audio_name'],
                audio_file=request.FILES['audio_file']
            ).save()
            messages.success(request, 'audio uploaded successfully!')
        else:
            messages.error(request, 'please fill all data!')
    company_id =Company_Info.objects.get(company_id=company_id)
    return render(request, 'add_audio.html',{'company_id':company_id})

@is_login
@feature_exist
@is_authorized
def add_video(request, company_id):
    if request.method == "POST":
        if 'video_url' in request.POST and 'video_name' in request.POST:
            inputVideoUrl = request.POST['video_url']
            yt = pytube.YouTube(inputVideoUrl)
            Company_videos(
                video_name=request.POST['video_name'], 
                video_link=yt.video_id, 
                company_id_id=company_id
            ).save()
            messages.success(request, 'video uploaded successfully!')
        else:
            messages.error(request, 'please fill all data!')
    company_id =Company_Info.objects.get(company_id=company_id)
    return render(request, 'add_video.html',{'company_id':company_id})

@is_login
@feature_exist
@is_unauthorized
def add_review(request, company_id):
    review = request.POST['review']
    star = request.POST['totalstar']
    if not star: star = 0
    try:
        user_review = Review.objects.get(user_id_id=request.user.user_id, company_id_id=company_id)
        user_review.review = review
        user_review.star = star
        user_review.save()
    except Review.DoesNotExist:
        Review(review=review, user_id_id=request.user.user_id, company_id_id=company_id,star=star).save()
    string = '/products/' + str(company_id)
    return redirect(string)



@is_login
@feature_exist
@is_authorized
def delete_company(request,company_id):
    Company_Info.objects.get(company_id=company_id).delete()
    messages.success(request,"company deleted succesfully!")
    return redirect('/')

@is_login
@feature_exist
@is_authorized
def delete_product_photo(request,product_photo_id):
    company = Company_Product_Photos.objects.get(company_product_photos_id=product_photo_id)
    string = "/products/" + str(company.company_id.company_id)
    company.delete()
    messages.success(request,"photo deleted succesfully!")
    return redirect(string)

@is_login
@feature_exist
@is_authorized
def delete_marketing_photo(request,marketing_photo_id):
    company = Company_Marketing_Photos.objects.get(company_Marketing_Photos_id=marketing_photo_id)
    string = "/products/" + str(company.company_id.company_id)
    company.delete()
    messages.success(request,"photo deleted succesfully!")
    return redirect(string)

@is_login
@feature_exist
@is_authorized
def delete_video(request,video_id):
    company = Company_videos.objects.get(company_videos_id=video_id)
    string = "/products/" + str(company.company_id.company_id)
    company.delete()
    messages.success(request,"video deleted succesfully!")
    return redirect(string)

@is_login
@feature_exist
@is_authorized
def delete_audio(request,audio_id):
    company_audio = Company_Audio.objects.get(pk=audio_id)
    string = "/products/" + str(company_audio.company.company_id)
    company_audio.delete()
    messages.success(request,"audio deleted succesfully!")
    return redirect(string)

@is_login
@feature_exist
@is_authorized
def delete_review(request, review_id):
    review = Review.objects.get(review_id=review_id)
    string = "/products/" + str(review.company_id.company_id)
    review.delete()
    return redirect(string)



@is_login
@feature_exist
@is_unauthorized
def likeImageOne(request, company_id):
    companyreview = Likes.objects.filter(company_id=company_id, user_id=request.user.user_id)
    if companyreview:
        companyreview[0].like = 1
        companyreview[0].save()
    else:
        data = Likes(like=1, company_id_id=company_id, user_id_id=request.user.user_id)
        data.save()
    return HttpResponse("Success!")

@is_login
@feature_exist
@is_unauthorized
def likeImageTwo(request, company_id):
    companyreview = Likes.objects.filter(company_id=company_id, user_id=request.user.user_id)
    if companyreview:
        companyreview[0].like = 2
        companyreview[0].save()
    else:
        Likes(like=1, company_id_id=company_id, user_id_id=request.user.user_id).save()
    return HttpResponse("Success!")

@is_login
@feature_exist
@is_unauthorized
def likeImageZero(request, company_id):
    companyreview = Likes.objects.get(company_id=company_id, user_id=request.user.user_id)
    companyreview.like = 0
    companyreview.save()
    return HttpResponse("Success!")


##############################################
# TO-DO TASK
# 1) add +91 in user registration form by default and let the user enter only 10 digit numbers