from django.shortcuts import render

# Create your views here.
def routePlanner(request):
    return render(request, 'planner/planner.html')