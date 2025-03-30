from django import forms
from .models import ChaiVariety, ChaiReview, Store

class StoreSearchForm(forms.Form):
    chai_type = forms.ChoiceField(
        choices=[('', 'All Chai Types')] + list(ChaiVariety.CHAI_TYPE_CHOICES),
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'placeholder': 'Select a chai type'
        })
    )

class ChaiReviewForm(forms.ModelForm):
    class Meta:
        model = ChaiReview
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(
                choices=[(i, str(i)) for i in range(1, 6)],
                attrs={'class': 'form-control'}
            ),
            'comment': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3}
            )
        }

#     class Meta:
#         model = Chai_varity
#         fields = ['chai_var']  # Updated to match the correct field name
