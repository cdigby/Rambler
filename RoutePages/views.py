from django.shortcuts import render
from RoutePlanner import models

def displayRoutePage(request, id):
    route = models.Route.objects.get(pk=id)
    routeDict = {
        'title': route.title,
        'description': route.description,
        'points': route.points,
        'length': round(route.length, 2),
        'image': route.image,
    }
    route.printRoute()
    return render(request, 'routePage.html', {'route': routeDict})

