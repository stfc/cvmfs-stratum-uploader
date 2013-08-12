import os
from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError
from guardian.admin import GuardedModelAdmin
from archer.projects.models import FileSystem, Project


class FileSystemAdminForm(forms.ModelForm):
    class Meta:
        model = FileSystem

    def clean_mount_point(self):
        mount_point = self.cleaned_data["mount_point"]
        if not os.path.exists(mount_point):
            raise ValidationError('%s does not exist!' % mount_point)
        if not os.path.isdir(mount_point):
            raise ValidationError('%s is not a directory!' % mount_point)
        if not os.access(mount_point, os.W_OK | os.X_OK):
            raise ValidationError('%s is not writable!' % mount_point)
        return mount_point


class ProjectAdmin(GuardedModelAdmin):
    list_display = ('__unicode__', 'file_system', 'directory')


class FileSystemAdmin(GuardedModelAdmin):
    list_display = ('__unicode__', 'alias', 'mount_point')
    form = FileSystemAdminForm


admin.site.register(FileSystem, admin_class=FileSystemAdmin)
admin.site.register(Project, admin_class=ProjectAdmin)
