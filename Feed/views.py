from django.shortcuts import render
from .models import Route
from django.shortcuts import get_object_or_404

import json
from django.http import HttpResponse

# Create your views here.
def display_feed(request):
    if (request.POST):
        jsonData = json.loads(request.body.decode())
        function = (jsonData['function'])
        if (function == "LIKE"):
            print ("LIKE")
        elif (function == "DISLIKE"):
            print ("DISLIKE")
        return HttpResponse("OK")
    else:
        print("########")

        route = Route.objects.get(pk=1)

        print(route.title)

        route_info = {
            'title': route.title,
            'description': route.description,
            'points': route.points,
            'rating': route.get_rating(),
        }

        return render(request, 'Feed/Feed.html', {'route': route_info})
