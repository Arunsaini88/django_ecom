from django.shortcuts import render

def Home(request):
    return render(request, 'home.html')

def Category(request):
    return render(request, 'oscar/catalogue/categories.html')

def Brand(request):
    return render(request, 'oscar/catalogue/brands.html')