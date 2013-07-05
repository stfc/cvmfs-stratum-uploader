# Create your views here.
from pprint import pprint
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse

from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, render_to_response
from django.template import loader
from django.template.context import RequestContext
from django.views.decorators.csrf import csrf_protect
from archer.uploader.forms import UploadFileForm
from archer.uploader.models import Package, CvmFs

NUMBER_OF_PACKAGES = 5


def index2(request):
    latest_packages = Package.objects.order_by('id')[:NUMBER_OF_PACKAGES]
    template = loader.get_template('packages/index.html')
    context = RequestContext(request, {
        'latest_packages': latest_packages,
    })
    return HttpResponse(template.render(context))


def index(request):
    latest_packages = Package.objects.order_by('-id')[:NUMBER_OF_PACKAGES]
    file_systems = CvmFs.objects.all()
    package_sets = dict([(fs, [package for package in fs.package_set.order_by('-id')]) for fs in file_systems])
    pprint(package_sets)
    context = {'latest_packages': latest_packages, 'package_sets': package_sets}
    return render(request, 'packages/index.html', context)


def show(request, package_id):
    package = get_object_or_404(Package, id=package_id)
    return render(request, 'packages/detail.html', {'package': package})


def upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # handle files
            pprint(form)
            package = form.save()
            package.status = 'uploaded'
            package.save()
            return HttpResponseRedirect('/')
    else:
        form = UploadFileForm()
    return render_to_response('packages/upload.html',
                              {'form': form},
                              context_instance=RequestContext(request))
