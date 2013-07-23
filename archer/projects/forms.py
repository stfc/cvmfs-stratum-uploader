from bootstrap_toolkit.widgets import BootstrapFileInput
from django import forms
from archer.packages.models import Package


class UploadFileForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = ['file']
        widgets = {
            'file': BootstrapFileInput(format_type='simple'),
        }

