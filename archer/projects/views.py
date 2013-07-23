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
    projects = get_objects_for_user2(request.user, 'projects.view_project')
    package_sets = [(project,
                     request.user.has_perm('projects.upload_package', project),
                     [package for package in project.package_set.order_by('-id')],
                    ) for project in projects]
    context = {'package_sets': package_sets, 'certs': certs}
    return render(request, 'projects/index.html', context)


@class_view_decorator(permission_required_or_403('projects.view_project', (Project, 'pk', 'project_id')))
class UploadView(View):
    def authorize(self, user, project_id):
        project = Project.objects.get(pk=project_id)
        if not user.has_perm('projects.upload_package', project):
            raise PermissionDenied

    def get(self, request, project_id):
        self.authorize(request.user, project_id)
        form = UploadFileForm()
        return render_to_response('projects/upload.html',
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
        return render_to_response('projects/upload.html',
                                  {'form': form, 'project_id': project_id},
                                  context_instance=RequestContext(request))


@permission_required_or_403('projects.view_project', (Project, 'pk', 'project_id'))
def show(request, project_id):
    project = Project.objects.get(pk=project_id)
    # if not request.user.has_perm('projects.view_project', project):
    #     raise PermissionDenied
    return render_to_response('projects/show.html',
                              {'project': project},
                              context_instance=RequestContext(request))