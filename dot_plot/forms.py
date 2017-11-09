from django import forms
from .models import *

class DotPlotForm(forms.ModelForm):

    first_sequence = forms.CharField()
    second_sequence = forms.CharField()
    sequence_type = forms.ChoiceField(choices=(('nucleotide','nucleotide'), ('aminoacids','aminoacids')))

    class Meta:
        model = DotPlot
        fields = '__all__'