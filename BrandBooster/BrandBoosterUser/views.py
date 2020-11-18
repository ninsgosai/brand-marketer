from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from BrandBoosterUser.forms import RegistrationForm,ChangePasswordOtpForm
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.forms import PasswordChangeForm,SetPasswordForm
from rest_framework.response import Response
from .models import *
from .serial import *
from .decorators import *
from Company.forms import RegistrationForm
import datetime
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from brandbooster.utils import send_email_for_user_account_activation,sendMail
from django.http import HttpResponse
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate

@api_view(['POST'])
def Account_Create(request):
    if 'login_type' in request.POST and request.POST['login_type']=="0":
        form = RegistrationForm(request.data)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                # user.set_password(user.password)
                user.is_active = False
                timestamp =  str(datetime.datetime.now())
                characters_to_remove = ":._- "
                for character in characters_to_remove:
                    timestamp = timestamp.replace(character, "")
                user.username =  timestamp
                send_email_for_user_account_activation(timestamp, user.email)
                user.mobile_code = request.POST['mobile_code']
                user.save()
                return Response({"error": 0, "data": [], "message": "Account has been created. Please check your email to activate your account."})
            except:
                user = Account.objects.filter(email=request.data['email'])
                if user: user[0].delete()
                return Response({"error": 17, "data": [], "message": "Please try again."})

        if 'email' in form.errors.as_data():
            if form.errors.as_data()['email'][0].code == "required":
                return Response({"error": 1, "data": [], "message": "User email may not be blank."})
            if form.errors.as_data()['email'][0].code == "invalid":
                return Response({"error": 2, "data": [], "message": "The email entered is not valid."})
            if form.errors.as_data()['email'][0].code == "unique":
                return Response({"error": 3, "data": [], "message": "User with this email already exist."})
        
        if 'mobile_number' in form.errors.as_data():
            if form.errors.as_data()['mobile_number'][0].code == 'required':
                return Response({"error": 4, "data": [], "message": "User phone number may not be blank."})
            if form.errors.as_data()['mobile_number'][0].code == "invalid_phone_number":
                return Response({"error": 5, "data": [], "message": "The phone number entered is not valid."})
            if form.errors.as_data()['mobile_number'][0].code == "unique":
                return Response({"error": 6, "data": [], "message": "User with this phone number already exist."})
        
        if 'password1' in form.errors.as_data():
            if form.errors.as_data()['password1'][0].code == 'required':
                return Response({"error": 7, "data": [], "message": "Password field may not be blank."})
        
        if 'password2' in form.errors.as_data():
            if form.errors.as_data()['password2'][0].code == 'required':
                return Response({"error": 8, "data": [], "message": "Confirm password field may not be blank."})
            if form.errors.as_data()['password2'][0].code == "password_too_similar":
                return Response({"error": 9, "data": [], "message": "The password cannot be too similar to the first name, last name, email."})
            if form.errors.as_data()['password2'][0].code == "password_too_short":
                return Response({"error": 10, "data": [], "message": "This password is too short. It must contain at least 8 characters."})
            if form.errors.as_data()['password2'][0].code == "password_mismatch":
                return Response({"error": 11, "data": [], "message": "The two password fields didn’t match."})
            if form.errors.as_data()['password2'][0].code == "password_entirely_numeric":
                return Response({"error": 12, "data": [], "message": "The password can not be entirely numbers."})
            if form.errors.as_data()['password2'][0].code == "password_too_common":
                return Response({"error": 13, "data": [], "message": "The password is too common."})
        
        if 'first_name' in form.errors.as_data():
            if form.errors.as_data()['first_name'][0].code == 'required':
                return Response({"error": 14, "data": [], "message": "First name may not be blank."})
        
        if 'last_name' in form.errors.as_data():
            if form.errors.as_data()['last_name'][0].code == 'required':
                return Response({"error": 15, "data": [], "message": "Last name may not be blank."})

        return Response({"error": 16, "data": [], "message": "Data is incorrect"})
    
    # FACEBOOK REGISTRATION
    elif 'login_type' in request.POST and request.POST['login_type']=='1':
        
        if 'facebook_token' not in request.POST:
            return Response({"error": 18, "data": [], "message": "Data is incorrect"})

        token = request.POST['facebook_token']

        if Account.objects.filter(facebook_token=token).exists(): 
            return Response({"error": 19, "data": [], "message": "This account already exist. Please login"})
        
        if 'email' in request.POST and request.POST['email'] != "":
            if Account.objects.filter(email=request.POST['email']).exists():
                return Response({"error": 20, "data": [], "message": "This email is already registered"})

        account = Account()
        account.login_type = 1
        account.facebook_token = token
        if 'email' in request.POST and request.POST['email'] != "": account.email = request.POST['email']
        if 'first_name' in request.POST: account.first_name = request.POST['first_name']
        if 'last_name' in request.POST: account.last_name = request.POST['last_name']
        account.save()

        serializer = Account_Serial(instance=account)
        return Response({"error": 0, "data": serializer.data, "message": "Registered succsesful"})

    # GOOGLE REGISTRATION
    elif 'login_type' in request.POST and request.POST['login_type']=='2':

        if 'email' not in request.POST or 'google_token' not in request.POST:
            return Response({"error": 21, "data": [], "message": "Data is incorrect"})
        
        email = request.POST['email'] 
        token = request.POST['google_token']
        
        if Account.objects.filter(google_token=token).exists(): 
            return Response({"error": 22, "data": [], "message": "This account already exist. Please login"})
        if Account.objects.filter(email=email).exists():
            return Response({"error": 23, "data": [], "message": "This email is already registered"})

        account = Account()
        account.login_type = 2
        account.email = email
        account.google_token = token
        if 'first_name' in request.POST: account.first_name = request.POST['first_name']
        if 'last_name' in request.POST: account.last_name = request.POST['last_name']
        account.save()
        serializer = Account_Serial(instance=account)
        return Response({"error": 0, "data": serializer.data, "message": "Registered succsesful"})

    else:
        return Response({"error": 24, "data": [], "message": "Data is incorrect"})


@api_view(['POST'])
def Account_Forget_Password(request):
    print("TEST")
    try:
        user = Account.objects.get(email=request.POST['email'])
        print(user.login_type)
        if user.login_type==1 or user.login_type==2:
            return Response({"error": 3, "data": [], "message": "Your Acount is either registered via gmail or facebook so you havn't any password"})
    except Account.DoesNotExist:
        return Response({"error": 1, "data": [], "message": "Account does not exist"})
    
    if request.POST['otp']:
        sendMail(request.POST['otp'],user.email)
        serializer = Account_Serial(instance=user)
        return Response({"error": 0, "data": serializer.data})
    else:
        return Response({"error": 2, "data": [], "message": "No Otp Found" })

@api_view(['POST'])
def Account_Change_Password(request):
    try:
        user = Account.objects.get(user_id=request.POST['user_id'])
    except Account.DoesNotExist:
        return Response({"error": 1, "data": [], "message": "Account does not exist."})
    
    user_authenticate = authenticate(username=user.email,password=request.POST['current_password'])
    if user_authenticate is not None:
        serializer = Change_Password_serial(instance=user,data=request.data)
        if serializer.is_valid():
            if request.POST['password'] == request.POST['password1']:
                user.password=make_password(request.POST['password'])
                user.save()
                return Response({"error": 0, "data": [], "message": "Password changed successfully."})
            else:
                return Response({"error": 2, "data": [], "message": "The two password fields didn't match."})
        if 'password' in serializer.errors:
            if serializer.errors['password'][0].code == "blank":
                return Response({"error": 3, "data": [], "message": "Password field may not be blank."})
            if serializer.errors['password'][0].code == "password_too_short":
                return Response({"error": 4, "data": [], "message": "This password is too short. It must contain at least 8 characters."})
            if serializer.errors['password'][0].code == "password_too_common":
                return Response({"error": 5, "data": [], "message": "The password cannot be too similar to the first name, last name, email."})
    else:
        return Response({"error": 6,"data": [],"message":"Old password does not match."})

    return Response({"error": 7,"data": [],"message":"Data is incorrect."})

@api_view(['POST'])
def Account_Forget_Change_Password(request):
    try:
        user = Account.objects.get(email=request.POST['email'])
    except Account.DoesNotExist:
        return Response({"error": 1, "data": [], "message": "Account does not exist."})
    serializer = Change_Password_serial(instance=user, data=request.data)

    if serializer.is_valid():
        if request.POST['password'] == request.POST['password2']:
            user.password=make_password(request.POST['password'])
            user.save()
            return Response({"error": 0, "data": [], "message": "Password changed successfully."})
        else:
            return Response({"error": 2, "data": [], "message": "The two password fields didn't match."})

    if 'password' in serializer.errors:
        if serializer.errors['password'][0].code == "blank":
            return Response({"error": 3, "data": [], "message": "Password field may not be blank."})
        if serializer.errors['password'][0].code == "password_too_short":
            return Response({"error": 4, "data": [], "message": "This password is too short. It must contain at least 8 characters."})
        if serializer.errors['password'][0].code == "password_too_common":
            return Response({"error": 5, "data": [], "message": "The password cannot be too similar to the first name, last name, email."})

    return Response({"error": 6, "data": [], "message": "Data is incorrect."})

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def Account_Update(request, pk):
    try:
        user = Account.objects.get(user_id=pk)
    except Account.DoesNotExist:
        return Response({"error": 1, "data": [], "message": "Account does not exist"})
    serializer = Account_Update_Serial(instance=user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        serializer = Account_Serial(instance=user)
        return Response({"error": 0, "data": serializer.data, })
    
    if 'first_name' in serializer.errors:
        if serializer.errors['first_name'][0].code == "blank":
            return Response({"error": 2, "data": [], "message": "First name may not be blank."})
    
    if 'last_name' in serializer.errors:
        if serializer.errors['last_name'][0].code == "blank":
            return Response({"error": 3, "data": [], "message": "Last name may not be blank."})
    
    if 'mobile_number' in serializer.errors:
        if serializer.errors['mobile_number'][0].code == 'blank':
            return Response({"error": 4, "data": [], "message": "User phone number may not be blank."})
        if serializer.errors['mobile_number'][0].code == "invalid_phone_number":
            return Response({"error": 5, "data": [], "message": "The phone number entered is not valid."})
        if serializer.errors['mobile_number'][0].code == "unique":
            return Response({"error": 6, "data": [], "message": "User with this phone number already exist."})
    if 'profile_photo' in request.FILES:
        if 'image' in request.FILES['profile_photo'].content_type:
            account = Account.objects.get(pk=pk)
            account.profile_photo = request.FILES['profile_photo']
            account.save()
        else:
            return Response({"error": 7, "data": [], "message": "Profile photo should be in valid image format."})

    return Response({"error": 8, "data": [], "message": "Data is incorrect"})

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def Account_Delete(request, pk):
    try:
        tasks = Account.objects.get(user_id=pk)
    except Account.DoesNotExist:
        return Response({"error": 1, "data": [], "message": "User does not exist."})
    
    tasks.delete()
    return Response({"error": 0, "message ": "Data Deleted"})

from Company.models import Company_Info
from Company.models import Company_videos
from Company.models import Company_Marketing_Photos
from Company.models import Company_Product_Photos
from Company.models import Company_Audio
from Company.models import Main_Slider
from Company.models import Category

from BrandBoosterUser.models import Account

def Logout_admin(request):
    logout(request)
    return render(request, 'admin/loginadmin.html')

@is_admin
def admin(request):
    a = Account.objects.count() - 1
    b = Company_Info.objects.count()
    c = Company_Marketing_Photos.objects.count()
    d = Company_videos.objects.count()
    e = Company_Product_Photos.objects.count()
    f = Company_Audio.objects.count()
    return render(request, 'admin/admin.html', {'a': a,'b': b,'c': c,'d': d,'e': e,'f':f})
    

@is_admin
def add_company_profile(request):
    x = Account.objects.all()
    if request.method == "GET":
        return render(request, 'admin/add_company_profile.html', {'x': x})

    companydom = request.POST['companydom']
    if Company_Info.objects.filter(company_domain=companydom):
        messages.add_message(request, messages.ERROR, 'This Domain Is Already Exists!!!')
        return render(request, 'admin/add_company_profile.html', {'x': x})
    
    companyemail = request.POST['companyemail']
    if Company_Info.objects.filter(company_email=companyemail):
        messages.add_message(request, messages.ERROR, 'This Email Is Already Exist!!!')
        return render(request, 'admin/add_company_profile.html', {'x': x})
    
    mobilenumber = request.POST['mobilenumber']
    # if len(mobilenumber) > 10 or len(mobilenumber) < 10:
    #     messages.add_message(request, messages.ERROR, 'Invalid Mobile Number!!!')
    #     return render(request, 'admin/add_company_profile.html', {'x': x})
    
    mobilenumber =  str(mobilenumber)
    if Company_Info.objects.filter(company_phone=mobilenumber):
        messages.add_message(request, messages.ERROR, 'This Mobile Number Is Already Exist!!!')
        return render(request, 'admin/add_company_profile.html', {'x': x})
    
    sel1 = request.POST['sel1']
    companyname = request.POST['companyname']
    companyinfo1 = request.POST['companyinfo1']
    companyinfo2 = request.POST['companyinfo2']

    companypincode = request.POST['companypincode']
    companycity = request.POST['companycity']
    companystate = request.POST['companystate']
    companyaddress = request.POST['companyaddress']
    if request.POST['phonenumber']:
        phonenumber = request.POST['phonenumber']


    
    if 'companyposter' in request.FILES:
        filevideo = request.FILES['companyposter']
    else:
        filevideo = request.POST['companyposter']
    if 'companyimage' in request.FILES:
        companyimage = request.FILES['companyimage']
    else:
        companyimage = request.POST['companyimage']
        
    if mobilenumber:
        myphone = Company_Info()
        myphone.company_phone = mobilenumber
    if 'company_whatsapp' in request.POST:
        whatsapp = Company_Info()
        whatsapp.company_whatsapp = request.POST['company_whatsapp']
    x = Company_Info(
            company_name=companyname,
            company_photo=companyimage,
            cover_image=filevideo,
            company_short_info=companyinfo1,
            company_long_info=companyinfo2,
            company_domain=companydom,
            company_city=companycity,
            company_state=companystate,
            company_address=companyaddress,
            company_telephone=phonenumber,
            company_pincode=companypincode,
            company_email=companyemail,
            company_phone= mobilenumber,
            company_phone_code= myphone.company_phone.country_code,
            company_whatsapp_code= whatsapp.company_whatsapp.country_code,
            user_id_id=sel1,
            company_status=True
    )
    x.save()
    x = Account.objects.all()
    messages.add_message(request, messages.SUCCESS, 'Your Company Is Addded')
    return render(request, 'admin/add_company_profile.html', {'x': x})

@is_admin
def add_photo(request):
    if request.method == "POST":
        companypic = request.FILES['companyimage']
        sel1 = request.POST['sel1']
        imagename = request.POST['imagename']
        x = Company_Product_Photos(company_prd_image=companypic, image_name=imagename, company_id_id=sel1)
        x.save()
        messages.add_message(request, messages.SUCCESS, 'Your photo is addded.')

    user = Company_Info.objects.all()
    return render(request, 'admin/add_photo.html', {'x': user})

@is_admin
def add_slider(request):
    if request.method == "POST":
        sliderimage = request.FILES['sliderimage']
        sliderinfo = request.POST['sliderinfo']
        slidername = request.POST['slidername']
        x = Main_Slider(slide_image=sliderimage, image_name=slidername, image_information=sliderinfo)
        x.save()
        messages.add_message(request, messages.SUCCESS, 'Your Slider is addded.')

    user = Main_Slider.objects.all()
    return render(request, 'admin/add_slider.html', {'x': user})

@is_admin
def add_category(request):
    if request.method == "POST":
        catname = request.POST['name']
        x = Category(name=catname)
        x.save()
        messages.add_message(request, messages.SUCCESS, 'Your Category is addded.')

    user = Category.objects.all()
    return render(request, 'admin/add_category.html', {'x': user})

@is_admin
def add_profile(request):
    if request.method == "POST":
        sel1 = request.POST['sel1']
        companyimage = request.FILES['companyimage']
        imagename = request.POST['imagename']
        y = Company_Marketing_Photos(company_mrk_image=companyimage, image_name=imagename, company_id_id=sel1)
        y.save()
        messages.add_message(request, messages.SUCCESS, 'Your marketing photo is addded.')
    
    x = Company_Info.objects.all()
    return render(request, 'admin/add_profile.html', {'x': x})

@is_admin
def add_video(request):
    if request.method == "POST":
        companyvideo = request.POST['myvideo']
        sel1 = request.POST['sel1']
        companyvideourl = companyvideo.replace("watch?v=", "embed/")
        companyimage = request.POST['videoimage']
        rest = companyvideourl.split("&", 1)[0]
        y = Company_videos(video_link=rest, video_name=companyimage, company_id_id=sel1)
        y.save()
        messages.add_message(request, messages.SUCCESS, 'Your video is added.')
    
    x = Company_Info.objects.all()
    return render(request, 'admin/add_video.html', {'x': x})

@is_admin
def add_audio(request):
    if request.method == "POST":
        companyaudio = request.FILES['companyaudio']
        sel1 = request.POST['sel1']
        audioname = request.POST['audioname']
        y = Company_Audio(audio_name=audioname, audio_file=companyaudio, company_id=sel1)
        y.save()
        messages.add_message(request, messages.SUCCESS, 'Your Audio is added.')
    
    x = Company_Info.objects.all()
    return render(request, 'admin/add_audio.html', {'x': x})
        
@is_admin
def update_company_profile(request):
    companydetail = Company_Info.objects.all()
    return render(request, 'admin/update_company_profile.html', {'companydetail': companydetail})

@is_admin
def update_photo(request):
    x = Company_Product_Photos.objects.all()
    return render(request, 'admin/update_photo.html', {'x': x})

@is_admin
def update_profile(request):
    x = Company_Marketing_Photos.objects.all()
    return render(request, 'admin/update_profile.html', {'x': x})

@is_admin
def update_audio(request):
    x = Company_Audio.objects.all()
    return render(request, 'admin/update_audio.html', {'x': x})

@is_admin
def update_video(request):
    x = Company_videos.objects.all()
    return render(request, 'admin/update_video.html', {'x': x})

@is_admin
def update_category(request):
    x = Category.objects.all()
    return render(request, 'admin/update_category.html', {'x': x})

@is_admin
def update_slider(request):
    x = Main_Slider.objects.all()
    return render(request, 'admin/update_slider.html', {'x': x})

@is_admin
def edit_video(request, pk):
    companyvideo = Company_videos.objects.get(company_videos_id=pk)
    if request.method == "GET":
        return render(request, 'admin/edit_video.html', {'x': companyvideo})
    
    companyvideo.video_name = request.POST['videoname']
    companyvideo.video_link = request.POST['videolink']
    companyvideo.video_link = companyvideo.video_link.replace("watch?v=", "embed/")
    companyvideo.save()
    messages.add_message(request, messages.SUCCESS, 'Your Video Is Edited')
    x = Company_videos.objects.all()
    return redirect('/home/update_video', {'companydetail': x})

@is_admin
def edit_audio(request, pk):
    companyaudio = Company_Audio.objects.get(id=pk)
    if request.method == "GET":
        return render(request, 'admin/edit_audio.html', {'x': companyaudio})
    
    companyaudio.audio_file = request.FILES['companyaudio']
    companyaudio.audio_name = request.POST['audioname']
    companyaudio.save()
    messages.add_message(request, messages.SUCCESS, 'Your Audio Is Edited')
    x = Company_Audio.objects.all()
    return redirect('/home/update_audio', {'x': x})

@is_admin
def edit_category(request, pk):
    category = Category.objects.get(id=pk)
    if request.method == "GET":
        return render(request, 'admin/edit_category.html', {'x': category})
    
    category.name = request.POST['name']
    category.save()
    messages.add_message(request, messages.SUCCESS, 'Your Category Is Edited')
    x = Category.objects.all()
    return redirect('/home/update_category', {'x': x})

@is_admin
def delete_video(request, pk):
    Company_videos.objects.get(company_videos_id=pk).delete()
    messages.add_message(request, messages.SUCCESS, 'Your Video Is Deleted')
    x = Company_videos.objects.all()
    return redirect('/home/update_video', {'x': x})

@is_admin
def delete_audio(request, pk):
    Company_Audio.objects.get(id=pk).delete()
    messages.add_message(request, messages.SUCCESS, 'Your Audio Is Deleted')
    x = Company_Audio.objects.all()
    return redirect('/home/update_audio', {'x': x})

@is_admin
def edit_company_profile(request, pk):
    companyinfo = Company_Info.objects.get(company_id=pk)
    if request.method == 'GET':
        return render(request, 'admin/edit_company_profile.html', {'companydetail': companyinfo})
    
    companydom = request.POST['companydom']
    if Company_Info.objects.filter(~Q(pk=pk), company_domain=companydom):
        messages.add_message(request, messages.ERROR, 'This Domain Is Already Exists!!!')
        return render(request, 'admin/edit_company_profile.html', {'companydetail': companyinfo})
    
    companyemail = request.POST['companyemail']
    if Company_Info.objects.filter(~Q(pk=pk), company_email=companyemail):
        messages.add_message(request, messages.ERROR, 'This Email Is Already Exist!!!')
        return render(request, 'admin/edit_company_profile.html', {'companydetail': companyinfo})
    
    mobilenumber = request.POST['companymobilenumber']
    # if len(mobilenumber) > 10 or len(mobilenumber) < 10:
    #     messages.add_message(request, messages.ERROR, 'Invalid Mobile Number!!!')
    #     return render(request, 'admin/edit_company_profile.html', {'companydetail': companyinfo})
    
    if Company_Info.objects.filter(~Q(pk=pk), company_phone=mobilenumber):
        messages.add_message(request, messages.ERROR, 'This Mobile Number Is Already Exist!!!')
        return render(request, 'admin/edit_company_profile.html', {'companydetail': companyinfo})

    companyinfo = Company_Info.objects.get(company_id=pk)
    companyinfo.company_name = request.POST['companyname']
    companyinfo.company_ceo = request.POST['companyceo']
    companyinfo.company_short_info = request.POST['companyinfo1']
    companyinfo.company_long_info = request.POST['companyinfo2']
    if 'slug' in request.POST:
        companyinfo.slug = request.POST['slug']
    companyinfo.company_domain = companydom
    companyinfo.company_email = companyemail
    companyinfo.company_phone = mobilenumber
    if companyinfo.company_phone:
        companyinfo.company_phone_code = companyinfo.company_phone.country_code
    companyinfo.company_whatsapp = request.POST['company_whatsapp']
    if companyinfo.company_whatsapp:
        companyinfo.company_whatsapp_code = companyinfo.company_whatsapp.country_code
    if 'coverimage' in request.FILES:
        companyinfo.cover_image = request.FILES['coverimage']
    if 'companyimage' in request.FILES:
        companyinfo.company_photo = request.FILES['companyimage']
    companyinfo.save()
    messages.add_message(request, messages.SUCCESS, 'Your Company Profile is Edited')
    return render(request, 'admin/edit_company_profile.html', {'companydetail': companyinfo})

@is_admin
def delete_company_profile(request, pk):
    Company_Info.objects.get(company_id=pk).delete()
    messages.add_message(request, messages.SUCCESS, 'Your Company Profile Is DELETED')
    companydetail = Company_Info.objects.all()
    return redirect('/home/update_company_profile', {'companydetail': companydetail})

@is_admin
def delete_photo(request, pk):
    Company_Product_Photos.objects.get(company_product_photos_id=pk).delete()
    messages.add_message(request, messages.SUCCESS, 'Your Photo Is Deleted')
    x = Company_Product_Photos.objects.all()
    return redirect('/home/update_photo', {'x': x})

@is_admin
def delete_slider(request, pk):
    Main_Slider.objects.get(id=pk).delete()
    messages.add_message(request, messages.SUCCESS, 'Your slider Is Deleted')
    x = Main_Slider.objects.all()
    return redirect('/home/update_slider', {'x': x})

@is_admin
def delete_category(request, pk):
    Category.objects.get(id=pk).delete()
    messages.add_message(request, messages.SUCCESS, 'Your category Is Deleted')
    x = Category.objects.all()
    return redirect('/home/update_category', {'x': x})

@is_admin
def edit_user(request, pk):
    userregister = Account.objects.filter(user_id=pk)
    if request.method == "GET":
        return render(request, 'admin/edit_user.html', {'userregister': userregister[0]})
    
    email = request.POST['email']
    if Account.objects.filter(~Q(pk=pk), email=email):
        messages.add_message(request, messages.ERROR, 'This Email Is Already Exist!!!')
        return render(request, 'admin/edit_user.html', {'userregister': userregister[0]})
    
    mobilenumber = request.POST['mobilenumber']
    if len(mobilenumber) > 10 or len(mobilenumber) < 10:
        messages.add_message(request, messages.ERROR, 'Invalid Mobile Number!!!')
        return render(request, 'admin/edit_user.html', {'userregister': userregister[0]})
    
    mobilenumber = str(mobilenumber)
    if Account.objects.filter(~Q(pk=pk), mobile_number=mobilenumber):
        messages.add_message(request, messages.ERROR, 'This Mobile Number Is Already Exist!!!')
        return render(request, 'admin/edit_user.html', {'userregister': userregister[0]})

    userregister = Account.objects.get(user_id=pk)
    userregister.first_name = request.POST['firstname']
    userregister.last_name = request.POST['lastname']
    userregister.email = email
    userregister.mobile_number = mobilenumber

    if 'profile_photo' in request.FILES:
        userregister.profile_photo = request.FILES['profile_photo']
    userregister.save()
    messages.add_message(request, messages.SUCCESS, 'Your User Is Edited')
    userregister = Account.objects.all()
    return redirect('/home/update_user', {'userregister': userregister})

@is_admin
def edit_photo(request, pk):
    addphoto = Company_Product_Photos.objects.get(company_product_photos_id=pk)
    if request.method == "GET":
        return render(request, 'admin/edit_photo.html', {'addphoto': addphoto})

    if bool(request.FILES.get('companyimage', False)) == True:
        imgInfo.company_prd_image = request.FILES['companyimage']
    imgInfo.image_name = request.POST['imagename']
    imgInfo.save()
    messages.add_message(request, messages.SUCCESS, 'Your Photo Is Edited')
    addphoto = Company_Product_Photos.objects.all()
    return redirect('/home/update_photo', {'addphoto': addphoto})

@is_admin
def edit_slider(request, pk):
    addphoto = Main_Slider.objects.get(id=pk)
    if request.method == "GET":
        return render(request, 'admin/edit_slider.html', {'addphoto': addphoto})

    imgInfo = Main_Slider.objects.get(id=pk)
    if bool(request.FILES.get('sliderimage', False)) == True:
        imgInfo.slide_image = request.FILES['sliderimage']
    imgInfo.image_name = request.POST['slidername']
    imgInfo.image_information = request.POST['sliderinfo']
    imgInfo.save()
    messages.add_message(request, messages.SUCCESS, 'Your Slider Is Edited')
    addphoto = Main_Slider.objects.all()
    return redirect('/home/update_slider', {'addphoto': addphoto})

@is_admin
def edit_profile(request, pk):
    addphoto = Company_Marketing_Photos.objects.get(company_Marketing_Photos_id=pk)
    if request.method == "GET":
        return render(request, 'admin/edit_profile.html', {'addphoto': addphoto})
    
    if bool(request.FILES.get('companyimage', False)) == True:
        addphoto.company_mrk_image = request.FILES['companyimage']
    addphoto.image_name = request.POST['imagename']
    addphoto.save()
    messages.add_message(request, messages.SUCCESS, 'Your marketing photo is edited.')
    addphoto = Company_Info.objects.all()
    return redirect('/home/update_profile', {'addphoto': addphoto})

@is_admin
def basic(request, pk):
    x = Account.objects.get(user_id=pk)
    return render(request, 'admin/add_user.html', {'x': x})

@is_admin
def main_profile(request, pk):
    i = Account.objects.get(user_id=pk)
    return render(request, 'admin/main_profile.html', {'companydetail': i})

@is_admin
def main_profile_edit(request, pk):
    x = Account.objects.filter(user_id=pk)
    if request.method == "GET":
        return render(request, 'admin/main_profile_edit.html', {'companydetail': x[0]})

    email = request.POST['email']
    if Account.objects.filter(~Q(pk=pk), email=email):
        messages.add_message(request, messages.ERROR, 'This Email Is Already Exist!!!')
        return render(request, 'admin/main_profile_edit.html', {'companydetail': x[0]})
    
    mobilenumber = request.POST['mobilenumber']
    # if len(mobilenumber) > 10 or len(mobilenumber) < 10:
    #     messages.add_message(request, messages.ERROR, 'Invalid Mobile Number!!!')
    #     return render(request, 'admin/main_profile_edit.html', {'companydetail': x[0]})

    if Account.objects.filter(~Q(pk=pk), mobile_number=mobilenumber):
        messages.add_message(request, messages.ERROR, 'This Mobile Number Is Already Exist!!!')
        return render(request, 'admin/main_profile_edit.html', {'companydetail': x[0]})

    z = Account.objects.get(user_id=pk)
    z.first_name = request.POST['firstname']
    z.last_name = request.POST['lastname']
    z.mobile_number = mobilenumber
    z.mobile_code = z.mobile_number.country_code
    z.email = email
    if bool(request.FILES.get('profile_photo', False)) == True:
        z.profile_photo = request.FILES['profile_photo']
    z.save()
    messages.add_message(request, messages.SUCCESS, 'Your Admin Profile Is Edited')
    return render(request, 'admin/main_profile_edit.html', {'companydetail': x[0]})

@is_admin
def main_profile_edit_password(request, pk):
    z = Account.objects.get(user_id=pk)

    if request.method == 'POST':
        pform = PasswordChangeForm(user=request.user, data=request.POST)
        if pform.is_valid():
            pform.save()
            logout(request)
            messages.add_message(request, messages.SUCCESS, 'Your password has been changed successfully.')
            return redirect(request, 'admin/main_profile_edit_password.html', {'i': z,'pform':pform})
        else:
            messages.add_message(request, messages.ERROR, 'your Password is not Changed')
            i = Account.objects.get(user_id=pk)
            return render(request, 'admin/main_profile_edit_password.html', {'i': z,'pform':pform})
    pform = PasswordChangeForm(user=request.user)
    return render(request, 'admin/main_profile_edit_password.html', {'i': z,'pform':pform})

@is_admin
def add_user(request):
    if request.method == "GET":
        return render(request, 'admin/add_user.html')

    firstname = request.POST['firstname']
    lastname = request.POST['lastname']
    email = request.POST['email']
    password = request.POST['password']
    password = make_password(password)
    
    if Account.objects.filter(email=email):
        messages.add_message(request, messages.ERROR, 'This email is already exist!!!')
        return render(request, 'admin/add_user.html')
    
    phonemumber = request.POST['inputMobile']
    # if len(phonemumber) > 10 or len(phonemumber) < 10:
    #     messages.add_message(request, messages.ERROR, 'Invalid mobile number!!!')
    #     return render(request, 'admin/add_user.html')
    
    phonemumber = str(phonemumber)
    if Account.objects.filter(mobile_number=phonemumber):
        messages.add_message(request, messages.ERROR, 'This mobile number is already exist!!!')
        return render(request, 'admin/add_user.html')
    
    x = Account(first_name=firstname, last_name=lastname, email=email, mobile_number=phonemumber, password=password)
    if bool(request.FILES.get('profile_photo', False)) == True:
        x.profile_photo = request.FILES['profile_photo']

    x.mobile_code=request.POST['mobile_code']
    x.save()
    messages.add_message(request, messages.SUCCESS, 'Your user is added successfully.')
    return render(request, 'admin/add_user.html')

@is_admin
def update_user(request):
    userregister = Account.objects.filter(~Q(user_id = request.user.user_id))
    return render(request, 'admin/update_user.html', {'companydetail': userregister})

@is_admin
def delete_profile(request, pk):
    Company_Marketing_Photos.objects.get(company_Marketing_Photos_id=pk).delete()
    messages.add_message(request, messages.SUCCESS, 'Your marketing photo is deleted.')
    x = Company_Marketing_Photos.objects.all()
    return redirect('/home/update_profile', {'x': x})

@is_admin
def delete_user(request, pk):
    Account.objects.get(user_id=pk).delete()
    messages.add_message(request, messages.SUCCESS, 'Your User Is Deleted')
    userregister = Account.objects.all()
    return redirect('/home/update_user/', {'userregister': userregister})

def loginadmin(request):
    if request.method == "POST":
        email = request.POST['Username']
        password = request.POST['Password']
        user = authenticate(email=email, password=password)
        if user and user.is_superuser:
            login(request, user)
            return redirect("admin")
        else:
            messages.add_message(request, messages.ERROR, 'Your User Or Password Is Invalid')
            return render(request, 'admin/loginadmin.html')
    else:
        # if request.user and request.user.is_superuser:
        #     login(request, request.user)
        #     return redirect("admin")
        return render(request, 'admin/loginadmin.html')

@is_admin
def ChangeCompanyStatus(request):
    if request.method=="POST":
        companyInfo = Company_Info.objects.get(company_id=request.POST['pk'])

        if companyInfo.company_status == True:
            companyInfo.company_status = False
        else:
            companyInfo.company_status = True
        companyInfo.save()
        return HttpResponse(request.POST['pk'])
    else:
        return HttpResponse("Request method is not a POST")

@is_admin
def ChangeUserStatus(request):
    if request.method=="POST":
        userInfo = Account.objects.get(user_id=request.POST['pk'])

        if userInfo.user_status == True:
            userInfo.user_status = False
        else:
            userInfo.user_status = True
        userInfo.save()
        return HttpResponse(request.POST['pk'])
    else:
        return HttpResponse("Request method is not a POST")