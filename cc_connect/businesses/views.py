from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder

from .models import Business
from .forms import BusinessSearchForm

import json

from .models import Business

def business_home(request):
    businesses = Business.objects.all()  # Fetch all businesses from the database
    return render(request, 'businesses/home.html', {'businesses': businesses})


def map(request):
    return render(request, 'businesses/map.html')

@login_required
def search(request):
    username = request.session.get('username', 'Guest')  # Retrieve username from session
    api_key = settings.GOOGLE_API_KEY 
    if request.method == 'POST':
        zip_code = request.POST.get('zipcode')
        business_type = request.POST.get('business_type')
        country = request.POST.get('country')

        businesses = Business.objects.filter(country__icontains=country)

        if zip_code:
            businesses = businesses.filter(address__icontains=zip_code)

        if business_type and business_type.lower() != 'all':
            businesses = businesses.filter(business_type__icontains=business_type)

        businesses_json = json.dumps(
            list(businesses.values('name', 'business_type', 'country', 'address', 'latitude', 'longitude')),
            cls=DjangoJSONEncoder,
            default=str
        )

        form = BusinessSearchForm(request.GET or None)

        return render(request, 'businesses/search_results.html', {
            'form': form,
            'businesses': businesses_json,
            'api_key': api_key,
        })

    return render(request, 'businesses/search.html')


def search_businesses(request):
    form = BusinessSearchForm(request.GET or None)
    businesses = Business.objects.all()
    api_key = settings.GOOGLE_API_KEY 

    if form.is_valid():
        zip_code = form.cleaned_data.get('zip_code')
        business_type = form.cleaned_data.get('business_type')
        country = form.cleaned_data.get('country')

        businesses = Business.objects.filter(country__icontains=country)

        if zip_code:
            businesses = businesses.filter(address__icontains=zip_code)

        if business_type and business_type.lower() != 'all':
            businesses = businesses.filter(business_type__icontains=business_type)

    businesses_json = json.dumps(
        list(businesses.values('name', 'business_type', 'country', 'address', 'latitude', 'longitude')),
        cls=DjangoJSONEncoder,
        default=str
    )
    
    return render(request, 'businesses/search_results.html', {
        'form': form,
        'businesses': businesses_json,
        'api_key': api_key,
    })