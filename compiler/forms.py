from django import forms
from compiler.models import CodeSubmission

# forms contains data which user has access to 

LANGUAGE_CHOICES = [
    ("py", "Python"),
    ("cpp", "C++"),
]


class CodeSubmissionForm(forms.ModelForm):
    language = forms.ChoiceField(choices=LANGUAGE_CHOICES)

    class Meta:
        model = CodeSubmission
        fields = ["language", "code", "input_data"]