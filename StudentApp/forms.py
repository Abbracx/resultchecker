from django import forms
from .models import Result, Candidate


class CandidateForm(forms.Form):
    exam_number = forms.CharField(max_length=10, help_text='enter examination number', required=True)
    class Meta:
        #model = Candidate
        fields = ['exam_num']
