from django import forms
from .models import Activity

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['name', 'description', 'start_date', 'end_date', 'location','latitude','longitude','image','person_limit', 'price_per_person']
       