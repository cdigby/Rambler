from django.shortcuts import render
from django.http import HttpResponse
import json
from . import models


# Create your views here.
def routePlanner(request):
    if request.method == 'GET':
        return render(request, 'planner/planner.html')
    elif request.method == 'POST':
        jsonData = json.loads(request.body.decode())
        title = (jsonData['title'])
        points = (jsonData['points'])
        route = models.Route()
        route.create_route(title, points)
        route.save()
        return HttpResponse("OK")



