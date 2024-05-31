from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout



@login_required
def profile_view(request):
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