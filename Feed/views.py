from django.shortcuts import render
from .models import Like, Dislike
from RoutePlanner.models import Route
from django.db import models
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

import json
from django.http import HttpResponse
from django.utils.timesince import timesince
from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank
from django.http import JsonResponse
from django.core import serializers


# Create your views here.
def display_feed(request):
    if request.is_ajax and request.method == 'POST':
        function = request.POST['function']
        route = request.POST['route']
        if (function == "LIKE"):
            remove_dislike(request.user.id, route)
            if (validate_like(request, route)):
                like = Like()
                like.create_like(route, request.user.id)
                like.save()

        elif (function == "DISLIKE"):
            remove_like(request.user.id, route)
            if (validate_dislike(request, route)):
                dislike = Dislike()
                dislike.create_dislike(route, request.user.id)
                dislike.save()

        #Update rating in db
        r = Route.objects.get(pk=route)
        r.update_rating()
        return JsonResponse({"rating": r.rating}, status=200)

    #Show latest routes by default otherwise show depending on search query
    else:
        #Handle requests for all routes sorted first
        if 'showall' in request.GET:
            sort = request.GET['showall']
            if sort == 'top' or sort ==  'new' or sort == 'old':
                return search_routes(request, '', 'routes', sort)
            else:
                return default_routes(request)

        #Check query exists and is not blank
        if 'query' in request.GET:
            #Search routes
            if request.GET['query'] != '':
                query = request.GET['query']
                target = request.GET['target']
                sort = request.GET['sort']
                return search_routes(request, query, target, sort)
                
            #Empty query, treat as default
            else:
                return default_routes(request)

        #Display default
        else:
            return default_routes(request)

#Render default routes
def default_routes(request):
    return search_routes(request, '', 'routes', 'new')

#Render searched routes
#   Takes 'routes', 'tags', 'description' or 'users' for target
#   Takes 'new', 'top' or 'old' for sort
def search_routes(request, query, target, sort):
    arr = []
    formatted_arr = []
    count = 0
    #Check db not empty
    if Route.objects.all().count() != 0:
        #All routes if no query
        if query == '':
            routes = Route.objects.all()

        #Search routes
        else:
            if target == 'routes':
                routes = Route.objects.filter(title__icontains=query)

            elif target == 'tags':
                #Convert query to lowercase and then split, as that is how tags are stored
                routes = Route.objects.filter(tags__contains=query.lower().split())

            elif target == 'description':
                #Use PostgreSQL's search engine to search for keywords in the description
                sq = SearchQuery(query)
                vector = SearchVector('description')
                #Search
                routes = Route.objects.annotate(search=vector).filter(search=sq).annotate(rank=SearchRank(vector, sq))

            elif target == 'users':
                routes = Route.objects.filter(user__exact=User.objects.get(username__iexact=query).id)

        #Sort routes
        if target != 'description':
            if sort == 'new':
                routes = routes.order_by('-date')
            
            elif sort == 'top':
                routes = routes.order_by('-rating')

            elif sort == 'old':
                routes = routes.order_by('date')

        #Handle description sorting
        else:
            if sort == 'new':
                routes = routes.order_by('-rank', '-date')
            
            elif sort == 'top':
                routes = routes.order_by('-rank', '-rating')

            elif sort == 'old':
                routes = routes.order_by('-rank', 'date')

        #Construct array
        for route in routes:
            route_info = {
                'title': route.title,
                'description': route.description,
                'points': route.points,
                'rating': route.rating,
                'id': route.id,
                'user': User.objects.get(pk=route.user).username,
                'date': timesince(route.date),
                'tags': route.tags,
            }
            arr.append(route_info)

        #Format array for rendering
        #Calculate number of pairs
        count = len(arr)
        even = False
        if count % 2 == 0:
            even = True
        
        pairs = 0
        if even:
            pairs = count // 2
        else:
            pairs = (count // 2) + 1

        #Split up array
        route_index = 0
        for i in range(pairs):
            #Check if last iteration on odd array
            if i == pairs - 1 and not even:
                formatted_arr.append([arr[route_index], None])
            else:
                formatted_arr.append([arr[route_index], arr[route_index + 1]])
            route_index += 2

    return render(request, 'Feed/Feed.html', {'routes': formatted_arr, 'query': query, 'target': target, 'sort': sort, 'count': count})

def validate_like(request, route):
    try:
        likes = Like.objects.filter(route=route, user=request.user.id).count()
        if (likes == 0):
            return True
        else:
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
