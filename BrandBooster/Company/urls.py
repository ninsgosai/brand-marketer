from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

from django.contrib.auth import views as auth_views
urlpatterns = [
    path('api/List_Category/',                              views.List_Category), 
    path('api/List_Company_By_Category/', views.List_Company_By_Category), 
    path('api/User_Company_List/<int:user_id>/',            views.User_Company_List),
    path('api/Company_Info_Detailed/<str:pk>/',             views.Company_Info_Detailed),
    path('api/Company_Info_View/',                          views.Company_Info_View),
    path('api/Company_Info_Create/',                        views.Company_Info_Create),
    path('api/Company_Info_Update/<str:pk>/',               views.Company_Info_Update),
    path('api/Company_Info_Delete/<str:pk>/',               views.Company_Info_Delete),

    path('api/Company_Marketing_Photos_View/<str:company_id>/', views.Company_Marketing_Photos_View),
    path('api/Company_Marketing_Photos_Create/',                views.Company_Marketing_Photos_Create),
    path('api/Company_Marketing_Photos_Delete/<str:pk>/',       views.Company_Marketing_Photos_Delete),

    path('api/Company_videos_View/<str:company_id>/',   views.Company_videos_View),
    path('api/Company_videos_Create/',                  views.Company_videos_Create),
    path('api/Company_videos_Delete/<str:pk>/',         views.Company_videos_Delete),

    path('api/Company_Product_Photos_View/<str:company_id>/',   views.Company_Product_Photos_View),
    path('api/Company_Product_Photos_Create/',                  views.Company_Product_Photos_Create),
    path('api/Company_Product_Photos_Delete/<str:pk>/',         views.Company_Product_Photos_Delete),

    path('api/Company_Audio_View/<str:company_id>/', views.Company_Audio_View),
    path('api/Company_Audio_Create/',                views.Company_Audio_Create),
    path('api/Company_Audio_Delete/<int:audio_id>/', views.Company_Audio_Delete),

    path('', views.home, name="home"),
    # path('products/<int:company_id>/',views.products, name="products"),
    path('products/<slug:slug>/',views.products, name="products"),
    
    path('add_company/', views.add_company, name="add_company"),
    path('edit_company/<int:company_id>/', views.edit_company, name="edit_company"),

    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='password_reset.html'),name='password_reset'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),name='password_reset_complete'),

    path('active/<str:username>/',views.active,name='active'),
    path('my_profile/', views.my_profile, name="my_profile"),
    path('edit_profile/', views.edit_profile, name="edit_profile"),
    path('my_company/', views.my_company, name="my_company"),
    path('change_password/',views.change_password, name="change_password"),
    path('logout/', views.logout_user, name="logout"),

    path('add_marketing_photo/<int:company_id>/', views.add_marketing_photo , name="add_marketing_photo"),
    path('add_product_photo/<int:company_id>/'  , views.add_product_photo   , name="add_product_photo"),
    path('add_audio/<int:company_id>/'          , views.add_audio           , name="add_audio"),
    path('add_video/<int:company_id>/'          , views.add_video           , name="add_video"),
    path('add_review/<int:company_id>/'         , views.add_review          , name="add_review"),

    path('delete_company/<int:company_id>/'                 , views.delete_company          , name="delete_company"),
    path('delete_product_photo/<int:product_photo_id>/'     , views.delete_product_photo    , name="delete_product_photo"),
    path('delete_marketing_photo/<int:marketing_photo_id>/' , views.delete_marketing_photo  , name="delete_marketing_photo"),
    path('delete_video/<int:video_id>/'                     , views.delete_video            , name="delete_video"),
    path('delete_audio/<int:audio_id>/'                     , views.delete_audio            , name="delete_audio"),
    path('delete_review/<int:review_id>/'                   , views.delete_review           , name="delete_review"),

    path('likeImageOne/<int:company_id>/',views.likeImageOne, name="likeImageOne"),
    path('likeImageTwo/<int:company_id>/',views.likeImageTwo, name="likeImageTwo"),
    path('likeImageZero/<int:company_id>/',views.likeImageZero, name="likeImageZero"),

]

