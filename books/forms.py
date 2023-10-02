from django import forms

from .models import Review

class BookReviewForm(forms.ModelForm):
    stars_given = forms.IntegerField(min_value=1, max_value=5)
    class Meta:
        model = Review
        fields = ('stars_given', 'comment')
