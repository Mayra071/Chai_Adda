from django import forms
from .models import Chai_varity

class Chai_varity_Form(forms.Form):
    chai_var = forms.ModelChoiceField(queryset=Chai_varity.objects.all(), label="Select Chai Variety")

#     class Meta:
#         model = Chai_varity
#         fields = ['chai_var']  # Updated to match the correct field name
