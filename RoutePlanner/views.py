from django.shortcuts import render
from django.http import HttpResponse
import json
import RoutePlanner


# Create your views here.
from .models import Route


def showRoute(request):
    route1 = Route.objects.get(pk=90)
    route = {
        'title': route1.title,
        'description': route1.description,
        'points': route1.points,
        'length': route1.length,
        'image': route1.image,
    }
    route1.printRoute()
    return render(request, 'planner/view.html', {'route': route})

def routePlanner(request):
    if request.method == 'GET':
        return render(request, 'planner/planner.html')
    elif request.method == 'POST':
        jsonData = json.loads(request.body.decode())
        title = (jsonData['title'])
        points = (jsonData['points'])
        description = (jsonData['description'])
        length = (jsonData['length'])
        image = (jsonData['image'])
        route = Route()
        route.create_route(title, points, description, length, image)
        route.save()

        return HttpResponse("OK")
"""
def feed(request):
    if request.method == 'GET':
        return render(request, 'addresss')
    elif request.method == 'POST':
        jsonData = json.loads(request.body.decode())
        operation = (jsonData['operation'])
        routeNo = (jsonData['routeNumber'])
        if (operation == "like"):
            #get model
            #change rating
            #save model
        elif (operation == "dislike"):
            # get model
            # change rating
            # save model
        return HttpResponse("OK")g
"""
def getRoutes(request):
    Routes =[]
    num_of_routes = Route.objects.all().count()
    print(num_of_routes)
    for i in range (num_of_routes):
        print(Route.objects.get(pk=1).title)

        #Routes.append({

         #   'title': Route.objects.get(pk=1).title

        #})
    return HttpResponse("OK")

