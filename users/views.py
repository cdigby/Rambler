from django.shortcuts import render
from django.contrib.auth.models import User

#Signup page
def signup_page(request):
    #Load page on GET
    if request.method == 'GET':
        return render(request, 'users/signup_page.html')

    #Create user on POST
    elif request.method == 'POST':
        username = request.user.username
        email = request.user.email
        password = request.user.password
        user = User.objects.create_user(username, email, password)

