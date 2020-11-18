# from rest_framework.decorators import permission_classes
# from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from .models import *
from .serial import *

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def review_company(request,company_id):
    try:
        company = Company_Info.objects.get(company_id=company_id)
    except Company_Info.DoesNotExist:
        return Response({"error": 1, "data" : [], "message" : "Company does not exist."})

    user_review = None
    all_reviews = Review.objects.filter(company_id=company)

    # CALCULATE AVERAGE STAR RATINGS
    review_count = all_reviews.count()
    total = 0
    average_rating = 0
    star_number = 0     
    if review_count != 0:
        for i in all_reviews:
            if i.star:
                total = total + i.star
                star_number += 1
        average_rating = int(total/star_number) if star_number else 0
        
    if 'user_id' in request.POST:
        try:
            user = Account.objects.get(user_id=request.POST['user_id'])
            user_review = Review.objects.get(user_id=user, company_id=company)
            if user_review:
                user_review_serial = Review_Serial(user_review)
                user_contex = { "review_id":user_review_serial.data['review_id'],
                                "review":user_review_serial.data['review'],
                                "star":user_review_serial.data['star'],
                                "date_time_created":user_review_serial.data['date_time_created'],
                                "date_time_modified":user_review_serial.data['date_time_modified'],
                                "user_id":user_review_serial.data['user_id'],
                                "company_id":user_review_serial.data['company_id'],
                                "first_name":user.first_name,
                                "profile_photo":user.profile_photo.url
                                }
            else:
                user_review_serial = None
        except Account.DoesNotExist:
            return Response({"error": 2, "data" : [], "message" : "User does not exist."})

        except Exception as e:
            user_contex = {}
        all_reviews = Review.objects.filter(~Q(user_id=user), company_id=company)
    else:
        user_contex = {}
    
    all_review_serializer = Review_Serial(all_reviews, many=True)
    allreview = {}
    allreviews = []
    if all_review_serializer:
        for i in all_reviews:
            allreview=({'review_id':i.review_id,
                      'review':i.review,
                      'star':i.star,
                      'date_time_created':str(i.date_time_created),
                      'date_time_modified':str(i.date_time_modified),
                      'user_id':i.user_id.user_id,
                      'first_name':i.user_id.first_name,
                      'profile_pic':i.user_id.profile_photo.url,
                      'company_id':i.company_id.company_id
                    })
            allreviews.append(allreview)

    return Response({"error": 0, "average_rating": average_rating, "user_data": user_contex, "data": allreviews})


@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def review_view(request,pk):
    try:
        review = Review.objects.get(review_id=pk)
    except Review.DoesNotExist:
        return Response({"error": 1, "data" : [], "message" : "Review does not exist."})
    serializer = Review_Serial(review)
    contex = {"review_id":serializer.data["review_id"],
                      "review":serializer.data["review"],
                      "star":serializer.data["star"],
                      "data_time_created":serializer.data["date_time_created"],
                      "date_time_modified":serializer.data["date_time_modified"],
                      "user_id":serializer.data["user_id"],
                      "company_id":serializer.data["company_id"],
                      "first_name":review.user_id.first_name,
                      "profile_photo":review.user_id.profile_photo.url
                      }
    return Response({"error": 0, "data" : contex })


@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def review_create(request):
    serializer = Review_Serial(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user_id = Account.objects.get(user_id=serializer.data["user_id"])
        contex = {"review_id":serializer.data["review_id"],
                      "review":serializer.data["review"],
                      "star":serializer.data["star"],
                      "data_time_created":serializer.data["date_time_created"],
                      "date_time_modified":serializer.data["date_time_modified"],
                      "user_id":serializer.data["user_id"],
                      "company_id":serializer.data["company_id"],
                      "first_name": user_id.first_name,
                      "profile_photo":user_id.profile_photo.url
                      }
        return Response({"error": 0, "data": contex})

    if 'non_field_errors' in serializer.errors:
        if serializer.errors['non_field_errors'][0].code == "unique":
            return Response({"error": 1, "data" : [], "message" : "User has already given review to this company"})
    
    if 'user_id' in serializer.errors:
        if serializer.errors['user_id'][0].code == "does_not_exist":
            return Response({"error": 2, "data" : [], "message" : "User does not exist."})
    
    if 'company_id' in serializer.errors:
        if serializer.errors['company_id'][0].code == "does_not_exist":
            return Response({"error": 3, "data" : [], "message" : "Company does not exist."})
    
    if 'review' in serializer.errors:
        if serializer.errors['review'][0].code == "blank":
            return Response({"error": 4, "data" : [], "message" : "Review may not be blank."})

    if 'star' in serializer.errors:
        if serializer.errors['star'][0].code == "invalid_choice":
            return Response({"error": 5, "data" : [], "message" : "Invalid star rating."})
    
    return Response({"error": 6, "data" : [], "message" : "Data is incorrect"})


@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def review_update(request, pk):
    try:
        tasks =Review.objects.get(review_id=pk)
    except Review.DoesNotExist:
        return Response({"error": 1, "data" : [], "message" : "Review does not exist."})

    serializer = Review_Update_Serial(instance=tasks, data=request.data)
    if serializer.is_valid():
        serializer.save()
        serializer = Review_Serial(instance=Review.objects.get(review_id=pk))
        contex = {"review_id":serializer.data["review_id"],
                      "review":serializer.data["review"],
                      "star":serializer.data["star"],
                      "data_time_created":serializer.data["date_time_created"],
                      "date_time_modified":serializer.data["date_time_modified"],
                      "user_id":serializer.data["user_id"],
                      "company_id":serializer.data["company_id"],
                      "first_name":tasks.user_id.first_name,
                      "profile_photo":tasks.user_id.profile_photo.url
                      }
        return Response({"error": 0, "data": contex})

    if 'review' in serializer.errors:
        if serializer.errors['review'][0].code == "blank":
            return Response({"error": 2, "data" : [], "message" : "Review may not be blank."})

    if 'star' in serializer.errors:
        if serializer.errors['star'][0].code == "invalid_choice":
            return Response({"error": 3, "data" : [], "message" : "Invalid star rating."})
    
    return Response({"error": 4, "data" : [], "message" : "Data is incorrect."})


@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def review_delete(request, pk):
    try:
        tasks = Review.objects.get(review_id=pk)
    except:
        return Response({"error": 1, "data" : [], "message" : "Review does not exist."})
    
    tasks.delete()
    return Response({"error": 0, "data" : [], "message" : "Review deleted"})

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def like_view(request):
    tasks = Likes.objects.filter(company_id=request.POST['company_id'], user_id=request.POST['user_id'])
    if tasks:
        return Response({"error": 0, "message": tasks[0].like})
    else:
        return Response({"error": 0, "message": 0})

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def like_user(request):
    try:
        user = Account.objects.get(user_id=request.POST['user_id'])
    except Account.DoesNotExist:
        return Response({"error": 1, "message": "User does not exist."})
    
    try:
        company = Company_Info.objects.get(company_id=request.POST['company_id'])
    except Company_Info.DoesNotExist:
        return Response({"error": 2, "message": "Company does not exist."})

    try:
        tasks = Likes.objects.get(company_id=company, user_id=user)
    except Likes.DoesNotExist:
        tasks = Likes(company_id=company, user_id=user, like=1)
        tasks.save()
        return Response({"error": 0, "message": 1})
    
    if tasks.like == 1:
        tasks.like = 0
        tasks.save()
        return Response({"error": 0, "message": 0})
    else:
        tasks.like = 1
        tasks.save()
        return Response({"error": 0, "message": 1})

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def dislike_user(request):
    try:
        user = Account.objects.get(user_id=request.POST['user_id'])
    except Account.DoesNotExist:
        return Response({"error": 1, "message": "User does not exist."})
    
    try:
        company = Company_Info.objects.get(company_id=request.POST['company_id'])
    except Company_Info.DoesNotExist:
        return Response({"error": 2, "message": "Company does not exist."})

    try:
        tasks = Likes.objects.get(company_id=company, user_id=user)
    except Likes.DoesNotExist:
        tasks = Likes(company_id=company, user_id=user, like=2)
        tasks.save()
        return Response({"error": 0, "message": 2})
    
    if tasks.like == 2:
        tasks.like = 0
        tasks.save()
        return Response({"error": 0, "message": 0})
    else:
        tasks.like = 2
        tasks.save()
        return Response({"error": 0, "message": 2})
