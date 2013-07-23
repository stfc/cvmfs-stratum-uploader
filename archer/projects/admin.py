from django.contrib import admin
from guardian.admin import GuardedModelAdmin
from archer.projects.models import FileSystem, Project


class ProjectAdmin(GuardedModelAdmin):
    list_display = ('file_system', 'directory')


class FileSystemAdmin(GuardedModelAdmin):
    pass


admin.site.register(FileSystem, admin_class=FileSystemAdmin)
admin.site.register(Project, admin_class=ProjectAdmin)
