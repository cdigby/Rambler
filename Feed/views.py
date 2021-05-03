from django.shortcuts import render
from .models import Route, Like, Dislike
from django.db import models
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

import json
from django.http import HttpResponse


# Create your views here.
def display_feed(request):
    if request.method == 'POST':
        jsonData = json.loads(request.body.decode())
        function = (jsonData['function'])
        route = (jsonData['route'])
        if (function == "LIKE"):
            print("LIKE")
            remove_dislike(request.user.id, route)
            #Dislike.objects.filter(route=route, user=request.user.id).delete()
            print(Dislike.objects.filter(route=route, user=request.user.id))
            if (validate_like(request, route)):
                like = Like()
                like.create_like(route, request.user.id)
                like.save()

            else:
                print("Already Liked")
        elif (function == "DISLIKE"):
            print("DISLIKE")
            remove_like(request.user.id, route)
            #Like.objects.filter(route=route, user=request.user.id).delete()
            print(Like.objects.filter(route=route, user=request.user.id))
            if (validate_dislike(request, route)):
                dislike = Dislike()
                dislike.create_dislike(route, request.user.id)
                dislike.save()

            else:
                print("Already Disliked")
        return HttpResponse("OK")
    else:
        routes = []
        count = Route.objects.all().count()
        if count != 0:
            for i in range(1, count + 1):
                print(i)
                route = Route.objects.get(pk=i)
                route_info = {
                    'title': route.title,
                    'description': route.description,
                    'points': route.points,
                    'rating': route.get_rating(),
                    'id': route.id,
                    'user': User.objects.get(pk=route.user).username,
                }
                routes.append(route_info)

        return render(request, 'Feed/Feed.html', {'routes': routes})


def validate_like(request, route):
    try:
        likes = Like.objects.filter(route=route, user=request.user.id).count()
        if (likes == 0):
            return True
        else:
            print("removing like")
            remove_like(request.user.id, route)
            return False
    except models.ObjectDoesNotExist:
        return True

def remove_like(user, route):
    Like.objects.filter(route=route, user=user).delete()

def validate_dislike(request, route):
    try:
        dislikes = Dislike.objects.filter(route=route, user=request.user.id).count()
        if (dislikes == 0):
            return True
        else:
            remove_dislike(request.user.id, route)
            return False
    except models.ObjectDoesNotExist:
        return True

def remove_dislike(user, route):
    Dislike.objects.filter(route=route, user=user).delete()
