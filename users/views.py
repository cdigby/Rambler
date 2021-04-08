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
        form = UserForm(request.POST)
        if form.is_valid():
            #Create user and login
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = User.objects.create_user(username, email, password)
            login(request, user)
            messages.success(request, "Welcome " + username + "!")
            return redirect('users:profile')
        else:
            #Show errors
            return render(request, 'users/signup_page.html', {"form": form})
    
    #Load page on GET
    else:
        form = UserForm()
        return render(request, 'users/signup_page.html', {"form": form})


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('users:login')

@login_required
def profile(request):
    u = request.user    
    initial_profile = {
        'username': u.username,
        'email': u.email,
    }

    #Update user details
    if request.method == 'POST':
        form = UserForm(request.POST, initial=initial_profile)
        if form.is_valid():
            #Get new data
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            #Update model
            u.username = username
            u.email = email

            #Change password if not empty
            if password != '':
                u.set_password(password)
                messages.success(request, "Saved profile and changed password!")
            else:
                messages.success(request, "Saved profile!")

            u.save()
            return redirect('users:profile')
        
        else:
            #Render profile with errors
            return render(request, 'users/profile.html', {'form': form})

    #Display user profile
    else:
        form = UserForm(initial=initial_profile)
        return render(request, 'users/profile.html', {'form': form})