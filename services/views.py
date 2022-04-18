from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Service

# Create your views here.
def home_page(request):
    if request.method == 'POST':
        Service.objects.create(name=request.POST['new_service'])
        return redirect('/')

    context = {'services': Service.objects.all()}
    return render(request, 'home.html', context)
