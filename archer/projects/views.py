import os
from pprint import pprint, pformat
import shutil
from django.contrib import messages

from django.core.urlresolvers import reverse

from django.http.response import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render, render_to_response, get_object_or_404
from django.template import loader
from django.utils.safestring import mark_safe
from guardian.decorators import permission_required_or_403
from django.template.context import RequestContext
from django.views.generic import View
import re
import guardian.shortcuts

from archer.core.decorators import class_view_decorator
from archer.projects.forms import UploadFileForm, MakeDirectoryForm, RemoveDirectoryForm
from archer.projects.models import Project
from archer.packages.models import Package

NUMBER_OF_PACKAGES = 5


def unauthenticated(request):
    return render(request, 'unauthenticated.html')


def get_objects_for_user(user, perms, klass=None, use_groups=True, any_perm=False):
    if user.is_authenticated():
        return guardian.shortcuts.get_objects_for_user(user, perms, klass, use_groups, any_perm)
    return []

def index(request):
    debug_info = {'user': pformat(request.user.__dict__),
                  'environ': pformat(dict(os.environ.items())),
                  'meta': pformat(dict(request.META))}
    projects = get_objects_for_user(request.user, 'projects.view_project')
    package_sets = [(project,
                     request.user.has_perm('projects.upload_package', project),
                     [package for package in project.package_set.order_by('-id')],
                    ) for project in projects]
    context = {'package_sets': package_sets, 'debug_info': debug_info}
    return render(request, 'projects/index.html', context)


@class_view_decorator(permission_required_or_403('projects.upload_package', (Project, 'pk', 'project_id')))
class UploadView(View):
    def get(self, request, project_id):
        form = UploadFileForm()
        return render_to_response('projects/upload.html',
                                  {'form': form, 'project_id': project_id},
                                  context_instance=RequestContext(request))

    def post(self, request, project_id):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            from guardian.shortcuts import assign_perm
            # handle files
            pprint(form)
            package = form.save(commit=False)
            package.status = Package.Status.uploaded
            package.project_id = project_id
            package.save()
            assign_perm('packages.deploy_package', request.user, package)
            assign_perm('packages.remove_package', request.user, package)
            return HttpResponseRedirect(reverse('projects:show', args=[project_id]))
        return render_to_response('projects/upload.html',
                                  {'form': form, 'project_id': project_id},
                                  context_instance=RequestContext(request))


class ModifyDirectory(View):
    def validate(self, project_id, path):
        if path.startswith('/'):
            raise ValueError('Directory "%s" cannot start with "/"' % path)
        project = Project.objects.get(pk=project_id)
        if re.search('(\.\./|/\.\.)', path):
            raise ValueError('%s contains ".."' % path)
        project_path = project.full_path()
        parent_directory = os.path.join(project_path, path)
        # if os.path.commonprefix([parent_directory, project_path]) != project_path:
        #     raise
        if not os.path.isdir(parent_directory):
            raise ValueError('"%s" is not a directory' % parent_directory)
        if not os.path.exists(parent_directory):
            raise ValueError('"%s" does not exist' % parent_directory)
        return project, parent_directory

# TODO: use django forms
@permission_required_or_403('projects.deploy_package', (Project, 'pk', 'project_id'))
def deploy(request, project_id, path):
    def validate():
        if path.startswith('/'):
            raise ValueError('Directory "%s" cannot start with "/"' % path)
        project = get_object_or_404(Project, pk=project_id)
        if re.search('(\.\./|/\.\.)', path):
            raise ValueError('%s contains ".."' % path)
        project_path = project.full_path()
        parent_directory = os.path.join(project_path, path)
        # if os.path.commonprefix([parent_directory, project_path]) != project_path:
        #     raise
        if not os.path.isdir(parent_directory):
            raise ValueError('"%s" is not a directory' % parent_directory)
        if not os.path.exists(parent_directory):
            raise ValueError('"%s" does not exist' % parent_directory)
        return project, parent_directory

    validate()
    if request.POST:
        if 'package' not in request.POST:
            return HttpResponseBadRequest()
        if not request.POST['package'].isdigit():
            messages.add_message(request, messages.ERROR,
                                 'package with id = "%s" does not exist!' % request.POST['package'])
            return HttpResponseRedirect(reverse('projects:deploy', args=[project_id, path]))
        package_id = request.POST['package']
        package = Package.objects.get(pk=package_id)

        if package.can_deploy():
            if request.user.has_perm('packages.deploy_package', package):
                try:
                    deployed = package.deploy(path)
                    if deployed:
                        messages.add_message(request, messages.SUCCESS,
                                             'Package "%s" successfully deployed in "%s" directory' % (package, path))
                    else:
                        messages.add_message(request, messages.ERROR, 'Cannot deploy a package "%s"!' % package)
                except (IOError, ValueError, OSError) as e:
                    messages.add_message(request, messages.ERROR,
                                         'Cannot deploy a package "%s": "%s"' % (package, e))
            else:
                messages.add_message(request, messages.ERROR,
                                     'Does not have permission to deploy package "%s"!' % package)
        else:
            messages.add_message(request, messages.ERROR, 'Cannot deploy a package "%s"!' % package)
        return HttpResponseRedirect(reverse('projects:show', args=[project_id]))

    else:
        projects_packages = Package.objects.filter(project_id=project_id)
        packages = [package for package in projects_packages if
                    request.user.has_perm('packages.deploy_package', package) and package.can_deploy()
        ]
        return render_to_response('projects/deploy.html',
                                  {'packages': packages,
                                   'project_id': project_id,
                                   'path': path,
                                  },
                                  context_instance=RequestContext(request))


@class_view_decorator(permission_required_or_403('projects.remove_directory', (Project, 'pk', 'project_id')))
class RemoveDirectory(ModifyDirectory):
    def common(self, project, parent):
        project_path = project.full_path()
        dir_to_delete = os.path.join(project_path, parent)
        if not os.path.isdir(dir_to_delete):
            raise ValueError('%s is not a directory' % dir_to_delete)
        if not os.path.exists(dir_to_delete):
            raise ValueError('%s does not exist' % dir_to_delete)

    def get(self, request, project_id, path):
        project, parent = self.validate(project_id, path)
        form = RemoveDirectoryForm(parent)
        try:
            self.common(project, parent)
            return render_to_response('projects/rmdir.html',
                                      {'project_id': project.id,
                                       'form': form,
                                       'path': path,
                                      },
                                      context_instance=RequestContext(request))
        except ValueError as e:
            messages.add_message(request, messages.ERROR, 'Could not delete directory: %s' % e)
            return HttpResponseRedirect(reverse('projects:show', args=[project_id]))

    def post(self, request, project_id, path):
        project, remove_directory = self.validate(project_id, path)
        form = RemoveDirectoryForm(remove_directory, request.POST)
        try:
            self.common(project, remove_directory)
            shutil.rmtree(remove_directory)
            messages.add_message(request, messages.SUCCESS,
                                 'Directory "%s" successfully removed.' % remove_directory)
        except (ValueError, OSError) as e:
            messages.add_message(request, messages.ERROR,
                                 'Could not delete directory "%s": %s' % (remove_directory, e))
        return HttpResponseRedirect(reverse('projects:show', args=[project_id]))


@class_view_decorator(permission_required_or_403('projects.make_directory', (Project, 'pk', 'project_id')))
class MakeDirectory(ModifyDirectory):
    def get(self, request, project_id, path):
        project, parent = self.validate(project_id, path)
        form = MakeDirectoryForm(parent)
        return render_to_response('projects/mkdir.html',
                                  {'project_id': project.id,
                                   'form': form,
                                   'path': path,
                                  },
                                  context_instance=RequestContext(request))

    def post(self, request, project_id, path):
        project, parent = self.validate(project_id, path)
        form = MakeDirectoryForm(parent, request.POST)
        if form.is_valid():
            try:
                new_directory = request.POST['new_directory']
                dir_full_path = os.path.join(parent, new_directory)
                os.mkdir(dir_full_path)
                messages.add_message(request, messages.SUCCESS,
                                     'Directory "%s" successfully created.' % dir_full_path)
            except OSError as e:
                messages.add_message(request, messages.ERROR,
                                     'Could not create directory "%s": %s' % (dir_full_path, e))
            return HttpResponseRedirect(reverse('projects:show', args=[project_id]))
        return render_to_response('projects/mkdir.html',
                                  {'form': form,
                                   'path': path,
                                   'project_id': project.id},
                                  context_instance=RequestContext(request))


@permission_required_or_403('projects.view_project', (Project, 'pk', 'project_id'))
def show(request, project_id, path=''):
    project = Project.objects.get(pk=project_id)
    can_upload = request.user.has_perm('projects.upload_package', project)
    can_deploy = request.user.has_perm('projects.deploy_package', project)
    path = project.full_path()

    def index_maker():
        def _index(root):
            # rfiles = []
            files = os.listdir(root)
            files_only = []
            relative_path = ''
            for mfile in files:
                full_file_path = root + '/' + mfile
                t = os.path.join(root, mfile)
                if os.path.isdir(t):
                    relative_path = full_file_path[len(path) + 1:]
                    yield loader.render_to_string('tree/_folder.html',
                                                  {'file': mfile + '/',
                                                   'subfiles': _index(os.path.join(root, t)),
                                                   'can_upload': can_upload,
                                                   'can_deploy': can_deploy,
                                                   'project_id': project_id,
                                                   'full_path': full_file_path,
                                                   'path': relative_path,
                                                  })
                    continue
                files_only += [mfile]
            if len(files_only) > 0:
                pre = len(files_only) > 50
                if pre:
                    files_only = "\n".join(files_only)
                yield loader.render_to_string('tree/_files.html',
                                              {'files': files_only,
                                               'project_id': project_id,
                                               'full_path': full_file_path,
                                               'path': relative_path,
                                               'pre': pre,
                                              })
                #         rfiles += ('dir', mfile + '/', index(os.path.join(root, t)))
                #     else:
                #         rfiles += ('file', mfile)
                # return rfiles

        if not os.path.isdir(path):
            return None
        return _index(path)

    return render_to_response('projects/show.html',
                              {'project': project,
                               'can_upload': can_upload,
                               'can_deploy': can_deploy,
                               'packages': [package for package in project.package_set.order_by('-id')],
                               'files': index_maker(),
                               'path': path,
                              },
                              context_instance=RequestContext(request))