from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home_page(request):
    context = {
        'new_service': request.POST.get('new_service', '')
    }
    return render(request, 'home.html', context)
