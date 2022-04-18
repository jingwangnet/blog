from django.shortcuts import render
from django.http import HttpResponse
from .models import Service

# Create your views here.
def home_page(request):
    if request.method == 'POST':
        service = Service.objects.create(name=request.POST['new_service'])
        new_service = service.name
    else:
        new_service = ''
    context = {
        'new_service': new_service 
    }
    return render(request, 'home.html', context)
