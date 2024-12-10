from django import forms
from .models import Activity

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['name', 'description', 'activity_date', 'location', 'latitude', 'longitude', 'price_per_person']
       