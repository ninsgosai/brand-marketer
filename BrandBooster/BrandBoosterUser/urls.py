from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    # API URL
    path('api/Account_Create/',            views.Account_Create),
    path('api/Account_Update/<str:pk>/',   views.Account_Update),
    path('api/Account_Delete/<str:pk>/',   views.Account_Delete),
    path('api/Account_Forget_Password/',   views.Account_Forget_Password),
    path('api/Account_Forget_Change_Password/',   views.Account_Forget_Change_Password),
    path('api/Account_Change_Password/',   views.Account_Change_Password),

    # ADMIN URL
    path('home/admin/', views.admin, name="admin"),
    path('home/loginadmin/',views.loginadmin,name = "loginadmin"),
    path('logoutAdmin', views.Logout_admin, name="logoutAdmin"),
    
    path('home/main_profile/<int:pk>/', views.main_profile, name="main_profile"),
    path('home/main_profile_edit/<str:pk>/', views.main_profile_edit, name="main_profile_edit"),
    path('home/main_profile_edit_password/<str:pk>/', views.main_profile_edit_password,name="main_profile_edit_password"),
    
    path('home/basic/<str:pk>/', views.basic, name="basic"),
    
    path('home/add_user/', views.add_user, name="add_user"),
    path('home/add_company_profile/', views.add_company_profile, name="add_company_profile"),
    path('home/add_photo/', views.add_photo, name="add_photo"),
    path('home/add_profile/', views.add_profile, name="add_profile"),
    path('home/add_video/', views.add_video, name="add_video"),
    path('home/add_audio/', views.add_audio, name="add_audio"),
    path('home/add_slider/', views.add_slider, name="add_slider"),
    path('home/add_category/', views.add_category, name="add_category"),

    path('home/edit_user/<str:pk>/', views.edit_user, name="edit_user"),
    path('home/edit_company_profile/<str:pk>/', views.edit_company_profile, name="edit_company_profile"),
    path('home/edit_photo/<str:pk>/', views.edit_photo, name="edit_photo"),
    path('home/edit_profile/<str:pk>/', views.edit_profile, name="edit_profile"),
    path('home/edit_video/<str:pk>/', views.edit_video, name="edit_video"),
    path('home/edit_audio/<str:pk>/', views.edit_audio, name="edit_audio"),
    path('home/edit_slider/<str:pk>/', views.edit_slider, name="edit_slider"),
    path('home/edit_category/<str:pk>/', views.edit_category, name="edit_category"),

    path('home/update_user/', views.update_user, name="update_user"),
    path('home/update_company_profile/', views.update_company_profile, name="update_company_profile"),
    path('home/update_photo/', views.update_photo, name="update_photo"),
    path('home/update_profile/', views.update_profile, name="update_profile"),
    path('home/update_video/', views.update_video, name="update_video"),
    path('home/update_audio/', views.update_audio, name="update_audio"),
    path('home/update_slider/', views.update_slider, name="update_slider"),
    path('home/update_category/', views.update_category, name="update_category"),


    path('home/delete_user/<str:pk>/', views.delete_user, name="delete_user"),
    path('home/delete_company_profile/<str:pk>/', views.delete_company_profile, name="delete_company_profile"),
    path('home/delete_photo/<str:pk>/', views.delete_photo, name="delete_photo"),
    path('home/delete_profile/<str:pk>/', views.delete_profile, name="delete_profile"),
    path('home/delete_video/<str:pk>/', views.delete_video, name="delete_video"),
    path('home/delete_audio/<str:pk>/', views.delete_audio, name="delete_audio"),
    path('home/delete_slider/<str:pk>/', views.delete_slider, name="delete_slider"),
    path('home/delete_category/<str:pk>/', views.delete_category, name="delete_category"),

    path('ChangeCompanyStatus', views.ChangeCompanyStatus, name="ChangeCompanyStatus"),
    path('ChangeUserStatus', views.ChangeUserStatus, name="ChangeUserStatus"),
]
