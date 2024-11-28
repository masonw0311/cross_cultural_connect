from django.shortcuts import render
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder

from .models import Business
from .forms import BusinessSearchForm

import json

def homepage(request):
    return render(request, 'businesses/home.html')

def map(request):
    return render(request, 'businesses/map.html')

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
    
    print(businesses_json)
    return render(request, 'businesses/search_results.html', {
        'form': form,
        'businesses': businesses_json,
        'api_key': api_key,
    })