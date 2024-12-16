from django import forms
from .models import Activity, Review
from django.utils.safestring import mark_safe

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['name', 'description', 'start_date', 'end_date', 'location','latitude','longitude','image','person_limit', 'price_per_person']


class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(1, 6)],
        widget=forms.Select(attrs={'class': 'rating-dropdown'}),
        label="Rate this activity:"
    )
    review_text = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Leave a comment (optional)'}),
        label="Review Text",
        required=False
    )
    class Meta:
        model = Review
        fields = ['rating', 'review_text']
