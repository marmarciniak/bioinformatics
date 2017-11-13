from django import forms
from .models import *

class DotPlotForm(forms.ModelForm):

    class Meta:
        model = DotPlot
        fields = '__all__'