from rest_framework.response import Response
from rest_framework.decorators import api_view
from BrandBoosterUser.models import Account
from django.contrib.auth import authenticate
from BrandBoosterUser.forms import AccountAuthenticationForm

@api_view(['POST'])
def login(request):
    logtype = request.POST['login_type']

    if logtype and logtype == '0':
        email = request.POST['email']
        password = request.POST['password']
        if Account.objects.filter(email=email).exists() and Account.objects.get(email=email).login_type != 0:
            return Response({"error": 3, "data": [], "message": "Your Acount is registered via social media. Please login from from your social media account only."})
        user = authenticate(email=email, password=password)
        
        if user:
            user = Account.objects.get(email=email)
            user.notification_token = request.POST['notification_token']
            data = {
                'user_id': user.user_id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'mobile_number': str(user.mobile_number),
                'mobile_code' : str(user.mobile_code),
                'is_admin': user.is_admin,
                'is_active': user.is_active,
                'date_joined': user.date_joined,
                'profile_photo': user.profile_photo.url,
                'notification_token': user.notification_token
            }
            return Response({"error": 0, "data": data})
            
        else:
            if Account.objects.filter(email=email, is_active=False):
                return Response({"error": 2, "message": "Please activate your account.", "data": []})
            return Response({"error": 1, "message": "Invalid login credentials", "data": []})
    
    elif logtype and logtype == '1':
        tok = request.POST['facebook_token']
        try:
            verify_token = Account.objects.get(facebook_token=tok)
            verify_token.notification_token = request.POST['notification_token']
        except:
            return Response({"error": 4, "message": "login failed try again.", "data": []})

        if verify_token.mobile_number is None:
            data = {
                    'user_id': verify_token.user_id,
                    'email': verify_token.email,
                    'first_name': verify_token.first_name,
                    'last_name': verify_token.last_name,
                    'mobile_number': "", 
                    'is_admin': verify_token.is_admin,
                    'is_active': verify_token.is_active,
                    'date_joined': verify_token.date_joined,
                    'profile_photo': verify_token.profile_photo.url,
                    'notification_token': verify_token.notification_token
                }
        else:
            data = {
                    'user_id': verify_token.user_id,
                    'email': verify_token.email,
                    'first_name': verify_token.first_name,
                    'last_name': verify_token.last_name,
                    'mobile_number': str(verify_token.mobile_number), 
                    'mobile_code' : verify_token.mobile_number.country_code,
                    'is_admin': verify_token.is_admin,
                    'is_active': verify_token.is_active,
                    'date_joined': verify_token.date_joined,
                    'profile_photo': verify_token.profile_photo.url,
                    'notification_token': verify_token.notification_token
                }
        return Response({"error": 0, "data": data})
    elif logtype and logtype == '2':
        tok = request.POST['google_token']
        try:
            verify_token = Account.objects.get(google_token=tok)
            verify_token.notification_token = request.POST['notification_token']
        except:
            return Response({"error": 5, "message": "login failed try again.", "data": []})
        if verify_token.mobile_number is None:
            data = {
                    'user_id': verify_token.user_id,
                    'email': verify_token.email,
                    'first_name': verify_token.first_name,
                    'last_name': verify_token.last_name,
                    'mobile_number': "", 
                    'is_admin': verify_token.is_admin,
                    'is_active': verify_token.is_active,
                    'date_joined': verify_token.date_joined,
                    'profile_photo': verify_token.profile_photo.url,
                    'notification_token': verify_token.notification_token
                }
        else:
            data = {
                    'user_id': verify_token.user_id,
                    'email': verify_token.email,
                    'first_name': verify_token.first_name,
                    'last_name': verify_token.last_name,
                    'mobile_number': str(verify_token.mobile_number), 
                    'mobile_code' : verify_token.mobile_number.country_code,
                    'is_admin': verify_token.is_admin,
                    'is_active': verify_token.is_active,
                    'date_joined': verify_token.date_joined,
                    'profile_photo': verify_token.profile_photo.url,
                    'notification_token': verify_token.notification_token
                }
        return Response({"error": 0, "data": data})

    else:
        return Response({"error": 3, "message": "Please provide logintype.", "data": []})