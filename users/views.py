from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignupForm, ProfileForm

#Signup page
def signup_view(request):
    #Load page on GET
    if request.method == 'GET':
        return render(request, 'users/signup_page.html', {"form": SignupForm()})

    #Create user on POST
    elif request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirmation = request.POST.get('password_confirmation')
    
        #Check passwords match
        if password != password_confirmation:
            ### Need to find some way of keeping entered data! ###
            messages.error(request, "Password and confirmation don't match!")
            return render(request, 'users/signup_page.html', {"form": SignupForm()})
        
        user = User.objects.create_user(username, email, password)
        login(request, user)
        return redirect('users:profile')


def logout_view(request):
    logout(request)
    return redirect('users:login')

@login_required
def profile(request):
    form = ProfileForm()
    return render(request, 'users/profile.html', {'form': form})