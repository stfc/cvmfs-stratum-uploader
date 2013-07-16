# Create your views here.
from archer.uploader.decorators import class_view_decorator
import os
from pprint import pprint, pformat
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, render_to_response
from django.template import loader
from django.template.context import RequestContext
from django.views.generic import View
from archer.uploader.forms import UploadFileForm
from archer.uploader.models import Package, FileSystem

NUMBER_OF_PACKAGES = 5


def unauthenticated(request):
    return render(request, 'unauthenticated.html')


@login_required
def index2(request):
    latest_packages = Package.objects.order_by('id')[:NUMBER_OF_PACKAGES]
    template = loader.get_template('packages/index.html')
    context = RequestContext(request, {
        'latest_packages': latest_packages,
    })
    return HttpResponse(template.render(context))


@login_required
def index(request):
    certs = pformat(dict(os.environ.items()))
    certs += "\n"
    certs += pformat(dict(request.META))
    certs += "\n"
    certs += pformat(request.user.__dict__)
    certs += "\n"
    certs += pformat(request.user)
    latest_packages = Package.objects.order_by('-id')[:NUMBER_OF_PACKAGES]
    file_systems = FileSystem.objects.all()
    package_sets = dict(
        [(project, [package for package in project.package_set.order_by('-id')]) for file_system in file_systems for
         project in file_system.project_set.order_by('-id')]
    )
    pprint(package_sets)
    context = {'latest_packages': latest_packages, 'package_sets': package_sets, 'certs': certs}
    return render(request, 'packages/index.html', context)


@login_required
def show(request, package_id):
    package = get_object_or_404(Package, id=package_id)

    return render(request, 'packages/show.html', {'package': package})


@login_required
def deploy(request, package_id):
    package = get_object_or_404(Package, id=package_id)

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


@class_view_decorator(login_required)
class UploadView(View):
    def get(self, request):
        form = UploadFileForm()
        return render_to_response('packages/upload.html',
                                  {'form': form},
                                  context_instance=RequestContext(request))

    def post(self, request):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # handle files
            pprint(form)
            package = form.save(commit=False)
            package.status = Package.Status.uploaded
            package.save()
            return HttpResponseRedirect('/')
        return render_to_response('packages/upload.html',
                                  {'form': form},
                                  context_instance=RequestContext(request))
