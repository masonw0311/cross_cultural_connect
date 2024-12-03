from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q  # Import Q for complex queries
from .models import Business
from .forms import BusinessSearchForm
import json

@login_required
def business_home(request):
    businesses = Business.objects.all()  # Fetch all businesses from the database
    return render(request, 'businesses/home.html', {'businesses': businesses})

@login_required
def map(request):
    businesses = Business.objects.values(
        'name',
        'business_type',
        'country',
        'address',
        'latitude',
        'longitude',
        'phone_number',
        'website',
        'image_url'
    )
    businesses_json = json.dumps(list(businesses), cls=DjangoJSONEncoder)
    
    return render(request, 'businesses/map.html', {
        'businesses': businesses_json,
    })



# @login_required
# def search(request):
#     username = request.session.get('username', 'Guest')  # Retrieve username from session
#     api_key = settings.GOOGLE_API_KEY
#     if request.method == 'POST':
#         zip_code = request.POST.get('zipcode')
#         business_type = request.POST.get('business_type')
#         country = request.POST.get('country')

#         businesses = Business.objects.filter(country__icontains=country)

#         if zip_code:
#             businesses = businesses.filter(address__icontains=zip_code)

#         if business_type and business_type.lower() != 'all':
#             businesses = businesses.filter(business_type__icontains=business_type)

#         businesses_json = json.dumps(
#             list(businesses.values('name', 'business_type', 'country', 'address', 'latitude', 'longitude','image_url')),
#             cls=DjangoJSONEncoder,
#             default=str
#         )

#         form = BusinessSearchForm(request.GET or None)

#         return render(request, 'businesses/search_results.html', {
#             'form': form,
#             'businesses': businesses_json,
#             'api_key': api_key,
#         })

#     return render(request, 'businesses/search.html')

@login_required
def search_businesses(request):
    query = request.GET.get('query', '')  # Retrieve the query parameter
    businesses = Business.objects.all()
    api_key = settings.GOOGLE_API_KEY

    if query:
        # Filter by name, zip code, or business type
        businesses = businesses.filter(
            Q(name__icontains=query) |  # Match name
            Q(address__icontains=query) |  # Match zip code in the address
            Q(business_type__icontains=query)  # Match business type
        )

    businesses_json = json.dumps(
        list(businesses.values('name', 'address', 'latitude', 'longitude', 'website')),
        cls=DjangoJSONEncoder
    )

    return render(request, 'businesses/search_results.html', {
        'businesses': businesses_json,
        'api_key': api_key,
    })
