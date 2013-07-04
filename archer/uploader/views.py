# Create your views here.

from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.template.context import RequestContext
from archer.uploader.models import Package

from bootstrap_toolkit.widgets import BootstrapUneditableInput

NUMBER_OF_PACKAGES = 5


def index2(request):
    latest_packages = Package.objects.order_by('id')[:NUMBER_OF_PACKAGES]
    template = loader.get_template('packages/index.html')
    context = RequestContext(request, {
        'latest_packages': latest_packages,
    })
    return HttpResponse(template.render(context))


def index(request):
    latest_packages = Package.objects.order_by('id')[:NUMBER_OF_PACKAGES]
    context = {'latest_packages': latest_packages}
    return render(request, 'packages/index.html', context)


def show(request, package_id):
    package = get_object_or_404(Package, id=package_id)
    return render(request, 'packages/detail.html', {'package': package})


def upload(request):
    return render(request, 'packages/upload.html')


def upload2(request):
    from pprint import pprint

    pprint(request.FILES)
    print request.FILES['myfile'] # this is my file
    return HttpResponse('asdqwe')
