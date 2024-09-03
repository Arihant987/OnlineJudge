# forms.py
from django import forms
from assignments.models import CodeRun

LANGUAGE_CHOICES = [
    ("py", "Python"),
    ("cpp", "C++"),
]

class CodeRunForm(forms.ModelForm):
    language = forms.ChoiceField(choices=LANGUAGE_CHOICES)

    class Meta:
        model = CodeRun
        fields = ["language", "code", "input_data"]