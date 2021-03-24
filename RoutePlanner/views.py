from django.shortcuts import render
from . import models


# Create your views here.
def routePlanner(request):
    if request.method == 'GET':
        return render(request, 'planner/planner.html')
    elif request.method == 'POST':
        title = request.route.title
        points = request.route.points
        route = models.Route.objects.create_route(title, points)



