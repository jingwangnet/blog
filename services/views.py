from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Service

# Create your views here.
def home_page(request):
    context = {'services': Service.objects.all()}
    return render(request, 'home.html', context)

def new_cate(request):
    Service.objects.create(name=request.POST['new_service'])
    return redirect('/services/the-only-url/')

def view_cate(request):
    context = {'services': Service.objects.all()}
    return render(request, 'view_category.html', context)
