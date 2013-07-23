import os
from pprint import pprint, pformat

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, render_to_response
from guardian.decorators import permission_required_or_403
from django.template.context import RequestContext
from django.views.generic import View
from guardian.shortcuts import get_objects_for_user
from django.core.exceptions import PermissionDenied

from archer.core.decorators import class_view_decorator
from archer.projects.forms import UploadFileForm
from archer.projects.models import Project
from archer.packages.models import Package


# @permission_required_or_403('packages.view_package', (Package, 'pk', 'package_id'))
def show(request, package_id):
    package = get_object_or_404(Package, id=package_id)
    return render(request, 'packages/show.html', {'package': package})

@permission_required_or_403('projects.deploy_packages')
def deploy(request, package_id):
    package = get_object_or_404(Package, id=package_id)

    project = Project.objects.get(pk=package.project_id)
    if not request.user.has_perm('projects.deploy_package', project):
        raise PermissionDenied

    if not package.can_deploy():
        messages.add_message(request, messages.ERROR, 'Cannot deploy a package!')
        return render(request, 'packages/show.html', {'package': package})
    else:
        for p in Package.objects.filter(status=Package.Status.deployed):
            p.status = Package.Status.undeployed
            p.save()
        try:
            result = package.deploy()
            if result:
                messages.add_message(request, messages.INFO, 'Package deployed!')
            else:
                messages.add_message(request, messages.ERROR, 'Error during deployment of the package.')
        except IOError as e:
            messages.add_message(request, messages.ERROR, 'Error during deployment of the package: ' + e.message)

        return render(request, 'packages/show.html', {'package': package})

@login_required
def remove(request, package_id):
    package = get_object_or_404(Package, id=package_id)

    if package.can_remove():
        if package.status == Package.Status.deployed:
            Package.clear_dir(package.project.full_path())
        try:
            if package.remove():
                messages.add_message(request, messages.INFO, 'Package file successfully deleted!')
            else:
                messages.add_message(request, messages.WARNING,
                                     'Package file was already deleted from the file system. Mark as deleted.')
        except IOError as e:
            messages.add_message(request, messages.ERROR, e.message)
    else:
        messages.add_message(request, messages.ERROR, 'Cannot delete package file!')
    return render(request, 'packages/show.html', {'package': package})
