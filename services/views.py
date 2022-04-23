from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Service, Category

# Create your views here.
def home_page(request):
    context = {'services': Service.objects.all()}
    return render(request, 'home.html', context)

def new_cate(request):
    category = Category.objects.create(
        name = request.POST['new_category_name'],
        abbr = request.POST['new_category_abbr'],
        resume = request.POST['new_category_resume']
    )
    Service.objects.create(
        name=request.POST['new_service_name'],
        resume=request.POST['new_service_resume'],
        category=category
    )
    return redirect(f'/services/{category.pk}/')

def view_cate(request, pk):
    category = Category.objects.get(pk=pk)
    services = Service.objects.filter(category=category)
    context = {'category': category}
    return render(request, 'view_category.html', context)

def add_ser(request, pk):
    category = Category.objects.get(pk=pk)
    Service.objects.create(
        name=request.POST['new_service_name'],
        resume=request.POST['new_service_resume'],
        category=category
    )
    return redirect(f'/services/{category.pk}/')
