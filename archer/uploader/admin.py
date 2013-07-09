from django.contrib import admin
from archer.uploader.models import FileSystem, Package, Project


class PackageAdmin(admin.ModelAdmin):
    # fieldsets = [
    #     (None, {'fields': ['file_path']}),
    #     ('Example Set of Fields', {'fields': ['project', 'status']}) # 'classes': ['collapse']
    # ]
    # list_display = ('project', 'file_path', 'status')
    list_display = ('project', 'file', 'status', 'created_at', 'updated_at')


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('file_system', 'directory', 'group')


admin.site.register(FileSystem)
admin.site.register(Project, admin_class=ProjectAdmin)
admin.site.register(Package, admin_class=PackageAdmin)
