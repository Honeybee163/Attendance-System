from django.shortcuts import render

# home page
def Home(request):
    return render(request, 'home.html')

def Contact(request):
    return render(request, 'contact.html')

def About(request):
    return render(request, 'about.html')
