from django.contrib import admin
from django.urls import path
from .views import *
urlpatterns = [
    path('api/review_company/<str:company_id>/',    review_company),
    path('api/review_view/<str:pk>/',               review_view),
    path('api/review_create/',                      review_create),
    path('api/review_update/<str:pk>/',             review_update),
    path('api/review_delete/<str:pk>/',             review_delete),
    path('api/like_view/',                          like_view),
    path('api/like_user/',                          like_user),
    path('api/dislike_user/',                       dislike_user)
]