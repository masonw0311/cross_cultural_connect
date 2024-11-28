from django.contrib import admin

from django.contrib import admin
from .models import Business

@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'business_type', 'address', 'phone_number', 'website', 'latitude', 'longitude')
    search_fields = ('name', 'country', 'business type', 'address', 'phone_number', 'website')
    list_filter = ('latitude', 'longitude', 'country', 'business_type')
