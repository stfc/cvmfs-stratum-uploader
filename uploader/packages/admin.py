from django.contrib import admin
from guardian.admin import GuardedModelAdmin
from uploader.packages.models import Package


class PackageAdmin(GuardedModelAdmin):
    actions = None

    list_display = ('project', 'file', 'status', 'uploaded_at', 'deployed_at')

    readonly_fields = ('project', 'file', 'status', 'uploaded_at', 'deployed_at')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(Package, admin_class=PackageAdmin)
