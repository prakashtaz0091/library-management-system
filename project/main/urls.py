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




    ########################################################################################
    #url paths for librarian user

    #add book
    path('books/', views.books_view, name='books_view'),

    #update book_data
    path('book/update/<str:book_id>', views.book_update, name='book_update'),

    #delete book_data
    path('book/delete/<str:book_id>', views.book_delete, name='book_delete'),

    #view book requests
    path('book/requests/', views.book_request_view, name='book_request_view'),


    #checkouts
    path('books/checkouts/', views.checkouts, name="checkouts"),


    ########################################################################################





    ########################################################################################

    #url paths for normal user

    #view books list for user
    path('user/books/', views.books_view_user, name='books_view_user'),

    #request a book
    path('request/book/<str:book_id>', views.add_book_request, name='add_book_request'),

    ########################################################################################

]