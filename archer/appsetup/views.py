# Create your views here.
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.http.response import HttpResponseBadRequest
from django.shortcuts import render
from guardian.decorators import permission_required_or_403
from archer.projects.models import Project, FileSystem
from archer.custom_auth.models import User
from forms import GrantAdminForm, FileSystemForm
import os


def index(request):
    show_admin = not User.superuser_exist()
    show_filesystems = FileSystem.can_setup(request.user)
    return render(request, 'appsetup/index.html', {'show_setup_admin': show_admin,
                                                   'show_setup_filesystems': show_filesystems,
    })


@login_required
def admin(request):
    if User.superuser_exist():
        messages.add_message(request, messages.ERROR, 'Cannot initialize the application. System admin already exists.')
        return HttpResponseRedirect(reverse('projects:index'))
    form = GrantAdminForm(request.POST)
    if request.method == 'GET':
        users = User.objects.all()
        return render(request, 'appsetup/admin.html', {'users': users})
    elif request.method == 'POST':
        if form.is_valid():
            try:
                user = request.user
                user.is_staff = True
                user.is_superuser = True
                user.save()
                messages.add_message(request, messages.SUCCESS, 'Admin privileges granted!')
                return HttpResponseRedirect(reverse('appsetup:index'))
            except (ValidationError, ) as e:
                messages.add_message(request, messages.ERROR, 'Failed to save user: %s' % e)

        return render(request, 'appsetup/admin.html', {'form': form, })
    else:
        return HttpResponseBadRequest()


@permission_required_or_403('projects.setup_filesystem')
def filesystems(request):
    if request.method == 'GET':
        form = FileSystemForm()
    elif request.method == 'POST':
        form = FileSystemForm(request.POST)
        if form.is_valid():
            file_system = form.save()
            messages.add_message(request, messages.SUCCESS, 'CVMFS mounting point "%s" has been created!' % file_system)
            return HttpResponseRedirect(reverse('appsetup:index'))
        else:
            pass
    else:
        return HttpResponseBadRequest()
    filesystems = FileSystem.objects.all()

    mount_point_candidates = ['/' + d for d in os.listdir('/')]
    mount_point_candidates = [d for d in mount_point_candidates if
                              os.path.isdir(d) and os.access(d, os.W_OK | os.X_OK) and
                              d not in [fs.mount_point for fs in filesystems]]

    return render(request, 'appsetup/filesystems.html',
                  {'form': form, 'filesystems': filesystems, 'mount_point_candidates': mount_point_candidates})
