from django.shortcuts import render
from django.http import HttpResponse

# home page
def Home(request):
    return render(request, 'home.html')

def Contact(request):
    return render(request, 'contact.html')

def About(request):
    return render(request, 'about.html')


def favicon(request):
    return HttpResponse(status=204)

