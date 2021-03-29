from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'users'
urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login_page.html'), name='login'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout_view, name='logout')
]