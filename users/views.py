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