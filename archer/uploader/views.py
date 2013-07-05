# Create your views here.
from pprint import pprint
from django.core.context_processors import csrf

from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, render_to_response
from django.template import loader
from django.template.context import RequestContext
from django.views.decorators.csrf import csrf_protect
from archer.uploader.forms import UploadFileForm
from archer.uploader.models import Package

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
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # handle files
            pprint(request.FILES)
            return HttpResponseRedirect('/')
    else:
        form = UploadFileForm()
    return render_to_response('packages/upload.html',   {'form': form}, context_instance=RequestContext(request))
