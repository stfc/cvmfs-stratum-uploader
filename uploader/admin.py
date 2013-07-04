from django.contrib import admin
from uploader.models import CvmFs, Package


class PackageAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['file_path']}),
        ('Example Set of Fields', {'fields': ['fs', 'status']}) # 'classes': ['collapse']
    ]
    list_display = ('fs', 'file_path', 'status')
    list_filter = ('fs', 'status')


admin.site.register(CvmFs)
admin.site.register(Package, PackageAdmin)