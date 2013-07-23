# Create your views here.
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

from archer.uploader.decorators import class_view_decorator

from archer.uploader.forms import UploadFileForm
from archer.uploader.models import Package, FileSystem, Project
from django.core.exceptions import PermissionDenied

NUMBER_OF_PACKAGES = 5


def unauthenticated(request):
    return render(request, 'unauthenticated.html')


def get_objects_for_user2(user, perms, klass=None, use_groups=True, any_perm=False):
    if user.is_authenticated():
        return get_objects_for_user(user, perms, klass, use_groups, any_perm)
    return []

def index(request):
    certs = u''
    certs += pformat(request.user.__dict__)
    certs += "\n"
    certs += pformat(request.user)
    certs += "\n"
    certs += pformat(dict(os.environ.items()))
    certs += "\n"
    certs += pformat(dict(request.META))
    projects = get_objects_for_user2(request.user, 'uploader.view_project')
    package_sets = [(project,
                     request.user.has_perm('uploader.upload_package', project),
                     [package for package in project.package_set.order_by('-id')],
                    ) for project in projects]
    context = {'package_sets': package_sets, 'certs': certs}
    return render(request, 'packages/index.html', context)


@class_view_decorator(permission_required_or_403('uploader.view_package', (Package, 'pk', 'package_id')))
def show_package(request, package_id):
    package = get_object_or_404(Package, id=package_id)
    return render(request, 'packages/show.html', {'package': package})


@class_view_decorator(permission_required_or_403('uploader.deploy_packages'))
def deploy(request, package_id):
    package = get_object_or_404(Package, id=package_id)

    project = Project.objects.get(pk=package.project_id)
    if not request.user.has_perm('uploader.deploy_package', project):
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


@class_view_decorator(permission_required_or_403('uploader.view_project', (Project, 'pk', 'project_id')))
class UploadView(View):
    def authorize(self, user, project_id):
        project = Project.objects.get(pk=project_id)
        if not user.has_perm('uploader.upload_package', project):
            raise PermissionDenied

    def get(self, request, project_id):
        self.authorize(request.user, project_id)
        form = UploadFileForm()
        return render_to_response('packages/upload.html',
                                  {'form': form, 'project_id': project_id},
                                  context_instance=RequestContext(request))

    def post(self, request, project_id):
        self.authorize(request.user, project_id)
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # handle files
            pprint(form)
            package = form.save(commit=False)
            package.status = Package.Status.uploaded
            package.project_id = project_id
            package.save()
            return HttpResponseRedirect('/')
        return render_to_response('packages/upload.html',
                                  {'form': form, 'project_id': project_id},
                                  context_instance=RequestContext(request))


@permission_required_or_403('uploader.view_project', (Project, 'pk', 'project_id'))
def show_project(request, project_id):
    project = Project.objects.get(pk=project_id)
    # if not request.user.has_perm('uploader.view_project', project):
    #     raise PermissionDenied
    return render_to_response('projects/show.html',
                              {'project': project},
                              context_instance=RequestContext(request))