from django import forms
from archer.uploader.models import Package
from archer.uploader.widgets import BootstrapFileInput

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = ['fs', 'file']
        widgets = {
            'file': BootstrapFileInput(),
        }

