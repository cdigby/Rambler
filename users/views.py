from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserForm

#Signup page
def signup_view(request):
    #Create user on POST
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirmation = request.POST.get('password_confirmation')
    
        #Check passwords match
        if password != password_confirmation:
            ### Need to find some way of keeping entered data! ###
            messages.error(request, "Password and confirmation don't match!")
            return render(request, 'users/signup_page.html', {"form": UserForm()})
        
        user = User.objects.create_user(username, email, password)
        login(request, user)
        return redirect('users:profile')
    
    #Load page on GET
    else:
        return render(request, 'users/signup_page.html', {"form": UserForm()})


def logout_view(request):
    logout(request)
    return redirect('users:login')

@login_required
def profile(request):
    #Update user details
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            #Save new details
            messages.success(request, "Profile updated successfully!")
            return redirect('users:profile')
        
        else:
            #Render profile with errors
            return render(request, 'users/profile.html', {'form': form})

    #Display user profile
    else:
        u = request.user    
        form = UserForm(initial={
            'username': u.username,
            'email': u.email,
        })
        return render(request, 'users/profile.html', {'form': form})