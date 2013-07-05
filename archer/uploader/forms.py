from bootstrap_toolkit.widgets import BootstrapTextInput, BootstrapDateInput
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
    title = forms.CharField(max_length=50,
                            help_text=u'This is the standard text input',
                            widget=BootstrapTextInput(prepend='PPP'), )

    date = forms.DateField(widget=BootstrapDateInput())

