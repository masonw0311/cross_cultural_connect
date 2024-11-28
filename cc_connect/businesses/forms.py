from django import forms

class BusinessSearchForm(forms.Form):
    zip_code = forms.CharField(max_length=10, required=False, label="ZIP Code")
    business_type = forms.CharField(max_length=100, required=False, label="Business Type", initial="All")
    country = forms.CharField(max_length=100, required=True, label="Country")