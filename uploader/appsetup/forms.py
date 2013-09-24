from django import forms
from uploader.projects.models import FileSystem
from uploader.custom_auth.models import User


class GrantAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']


class FileSystemForm(forms.ModelForm):
    class Meta:
        model = FileSystem
        fields = ['alias', 'mount_point']
