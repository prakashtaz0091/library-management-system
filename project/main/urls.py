from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),


    #authentication
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/signup/', views.signup_view, name='signup'),
    path('accounts/logout/', views.logout_view, name='logout'),


    #profile
    path('profile/', views.profile_view, name="profile"),

    #upload profile pic
    path('profile-picture/upload/', views.profile_pic_upload, name="profile_pic_upload"),
]