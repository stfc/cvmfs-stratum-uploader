from bootstrap_toolkit.widgets import BootstrapFileInput
from django import forms
from archer.uploader.models import Package


class UploadFileForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = ['project', 'file']
        widgets = {
            'file': BootstrapFileInput(format_type='simple'),
        }

