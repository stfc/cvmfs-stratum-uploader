from django.contrib import admin
from guardian.admin import GuardedModelAdmin
from archer.packages.models import Package


class PackageAdmin(GuardedModelAdmin):
    list_display = ('project', 'file', 'status', 'created_at', 'updated_at')

    readonly_fields = ('project', 'file', 'status', 'deployed_at')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(Package, admin_class=PackageAdmin)
