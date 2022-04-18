from django.shortcuts import render
from django.http import HttpResponse
from .models import Service

# Create your views here.
def home_page(request):
    service = Service() 
    service.name = request.POST.get('new_service', '')
    service.save()
    context = {
        'new_service': service.name
    }
    return render(request, 'home.html', context)
