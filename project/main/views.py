from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from . helpers import is_valid_phone_number
from django.views.decorators.http import require_http_methods

from . import models




@require_http_methods(["POST"])
@login_required
def profile_pic_upload(request):
    print(request.method,"*****************************")
    if request.method == "POST":
        image = request.FILES.get('profile_img')

        if image:
            try:
                profile = models.Profile.objects.get(user=request.user)
            except models.Profile.DoesNotExist:
                profile = models.Profile.objects.create(user=request.user)

            if profile:
                profile.image = image
                profile.save()
                messages.success(request, 'Profile picture updated successfully')
                return redirect('main:profile', permanent=True)
            else:
                messages.error(request, 'Error updating profile picture, profile not found')
                return redirect('main:profile', permanent=True)    
        
        else:
            messages.error(request, 'Error updating profile picture')
            return redirect('main:profile', permanent=True)
            

    


@login_required
def profile_view(request):
    if request.method=="POST":
        # print(request.POST)
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        mobile_number = request.POST['mobile_number']




        if not is_valid_phone_number(mobile_number):
            messages.error(request, 'Please enter a valid phone number')
            return redirect('main:profile', permanent=True)

        if (request.user.first_name == "" or request.user.last_name == ""):
            if len(first_name) < 2  or len(last_name) < 2:
                messages.error(request, 'First and last names must be at least 2 characters long')
                return redirect('main:profile', permanent=True)



        user = request.user
        user.first_name = first_name if first_name!="" else user.first_name
        user.last_name = last_name if last_name!="" else user.last_name
        user.save()

        try:
            profile = models.Profile.objects.get(user=request.user)
            profile.mobile_number = mobile_number
            profile.save()
        except models.Profile.DoesNotExist:
            models.Profile.objects.create(
                user=user,
                mobile_number=mobile_number
            )

        messages.success(request, 'Profile updated successfully')
        return redirect('main:profile', permanent=True)


    return render(request, 'main/profile.html')


@login_required
def dashboard(request):
    return render(request, 'main/dashboard.html')



def login_view(request):

    if request.method == "POST":
        data = request.POST

        username = data['username']
        password = data['password']

        # user = User.objects.filter(username=username).first()
        user = authenticate(request, username=username, password=password)

        if user:
            # if user.check_password(password):  #you can use this too
            login(request, user)
            return redirect('main:dashboard')
            
        else:
            messages.error(request, 'Invalid Credentials')

            return redirect("main:login")


    return render(request, 'main/login.html')







def signup_view(request):

    if request.method == "POST":
        data = request.POST

        username = data['username']

        #check if username already exists
        try:
            User.objects.get(username=username)

            #generate auto username using random module and use your own creative logic

            messages.error(request, f'User with {username} already exists, try another username')
        except User.DoesNotExist:
             #username validation    
            if len(username) < 6:
                messages.error(request, 'Username must be at least 6 characters long')

                context = {
                    'old_data': data,
                }
                return render(request, 'main/signup.html', context)
            

            #password length validation
            if len(data['password']) < 6:
                messages.error(request, 'Password must be at least 6 characters long')

                context = {
                    'old_data': data,
                }
                return render(request, 'main/signup.html', context)
            
            else:
                #password match validation
                if data['password'] != data['confirm_password']:
                    messages.error(request, 'Password and Confirm Password do not match')

                    context = {
                        'old_data': data,
                    }
                    return render(request, 'main/signup.html', context)
                
            #user data is valid, lets create user in database

            user = User.objects.create_user(data['username'], data['email'], data['password'])

            # user.save()s

            messages.success(request, f'Account for {user.username} created successfully')

            return redirect("main:login")



    return render(request, 'main/signup.html')




def logout_view(request):
    logout(request)
    return redirect("main:login")