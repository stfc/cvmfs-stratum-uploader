from django.contrib import admin
from guardian.admin import GuardedModelAdmin
from archer.projects.models import FileSystem, Project


class ProjectAdmin(GuardedModelAdmin):
    list_display = ('__unicode__', 'file_system', 'directory')


class FileSystemAdmin(GuardedModelAdmin):
    list_display = ('__unicode__', 'alias', 'mount_point')


admin.site.register(FileSystem, admin_class=FileSystemAdmin)
admin.site.register(Project, admin_class=ProjectAdmin)
