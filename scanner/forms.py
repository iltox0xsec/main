
from django import forms
import re

RECORD_CHOICES = [
    ('A', 'A'),
    ('AAAA', 'AAAA'),
    ('CNAME', 'CNAME'),
    ('MX', 'MX'),
    ('NS', 'NS'),
    ('TXT', 'TXT'),
]

class DomainForm(forms.Form):
    domain = forms.CharField(max_length=255, label='Domain')
    record_types = forms.MultipleChoiceField(
        choices=RECORD_CHOICES, 
        widget=forms.CheckboxSelectMultiple,
        label='Record Types'
    )
    all_records = forms.BooleanField(required=False, label='All Records')

    def clean_domain(self):
        domain = self.cleaned_data.get('domain')
        domain_regex = re.compile(
            r'^(?!:\/\/)([a-zA-Z0-9-_]{1,63}\.)+[a-zA-Z]{2,6}$'
        )
        if not domain_regex.match(domain):
            raise forms.ValidationError("Please enter a valid domain name.")
        return domain