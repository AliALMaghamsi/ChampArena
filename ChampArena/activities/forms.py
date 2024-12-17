from django import forms
from .models import Activity, ActivityCategory , ActivityName


class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['name', 'description', 'start_date', 'end_date', 'location','latitude','longitude','image','person_limit', 'price_per_person']
       
class ActivityCategoryForm(forms.ModelForm):
    class Meta:
        model = ActivityCategory
        fields = ['name']

class ActivityNameForm(forms.ModelForm):
    class Meta:
        model=ActivityName
        fields = '__all__'
       