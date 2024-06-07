from django import forms
from django.core.validators import FileExtensionValidator


class EmlUploadForm(forms.Form):
    eml_file = forms.FileField(validators=[FileExtensionValidator(allowed_extensions=['eml'])], widget=forms.ClearableFileInput(attrs={'accept': '.eml'}))

    def clean_eml_file(self):
        eml_file = self.cleaned_data.get('eml_file')
        if not eml_file.name.endswith('.eml'):
            raise forms.ValidationError("ONLY .eml")
        return eml_file

class UploadAnyFileForm(forms.Form):
    file = forms.FileField()