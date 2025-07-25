from django.shortcuts import render

def index(request):
    """View for the main prediction page"""
    return render(request, 'myapp/index.html')
