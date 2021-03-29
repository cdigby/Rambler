from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django import forms

#Define signup form
class SignupForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput())
    password_confirmation = forms.CharField(widget=forms.PasswordInput())

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
            error = "Password and confirmation don't match!"
            ### Need to find some way of keeping entered data! ###
            return render(request, 'users/signup_page.html', {"form": SignupForm(), "error": error})
        
        user = User.objects.create_user(username, email, password)
        return redirect('users:profile')


def logout_view(request):
    logout(request)
    return redirect('users:login')

@login_required
def profile(request):
    return render(request, 'users/profile.html', {"current_user": request.user})