# Create your views here.
import os

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.http.response import HttpResponseBadRequest
from django.shortcuts import render
from guardian.decorators import permission_required_or_403

from archer.projects.models import FileSystem
from archer.custom_auth.models import User
from forms import GrantAdminForm, FileSystemForm


def index(request):
    show_admin = not User.superuser_exist()
    show_filesystems = FileSystem.can_setup(request.user)
    return render(request, 'appsetup/index.html', {'show_setup_admin': show_admin,
                                                   'show_setup_filesystems': show_filesystems,
    })


def admin(request):
    if User.superuser_exist():
        user = request.user
        if user.is_authenticated():
            messages.add_message(request, messages.ERROR,
                                 'Cannot initialize the application. System admin already exists.')
        return HttpResponseRedirect(reverse('index'))

    if request.method == 'POST':
        form = GrantAdminForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.is_active = True
                user.is_staff = True
                user.is_superuser = True
                user.save()
                messages.add_message(request, messages.SUCCESS, 'Admin privileges granted!')
                return HttpResponseRedirect(reverse('appsetup:index'))
            except (ValidationError, ) as e:
                messages.add_message(request, messages.ERROR, 'Failed to save user: %s' % e)
    else:
        form = GrantAdminForm()
    users = User.objects.all()
    return render(request, 'appsetup/admin.html',
                  {'form': form, 'users': users, 'current_dn': request.META['REMOTE_USER']}, )


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
