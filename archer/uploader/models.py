import os
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


class FileSystem(models.Model):
    mount_point = models.CharField(max_length=2000, null=False, blank=False, unique=True)

    def __unicode__(self):
        return self.mount_point


class Project(models.Model):
    file_system = models.ForeignKey(FileSystem)
    directory = models.CharField(max_length=200, null=False, blank=False)
    user = models.ForeignKey(User, null=True, blank=True, unique=True)

    class Meta:
        unique_together = ('file_system', 'directory')

    def __unicode__(self):
        return os.path.join(str(self.file_system), str(self.directory))


class Package(models.Model):
    def __get_upload_path(instance, filename):
        return os.path.join(settings.MEDIA_ROOT, ".%s" % instance.project, filename)

    STATUSES = [(a, a) for a in ['new', 'uploaded', 'unpacking', 'deployed', 'cancelled', 'deleted']]
    STATUSES_LENGTH = 10 # max(STATUSES, key=len)
    project = models.ForeignKey(Project)
    file = models.FileField(upload_to=__get_upload_path)
    status = models.CharField(max_length=STATUSES_LENGTH, choices=STATUSES, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return 'Package[project=' + str(self.project) + ', file=' + str(self.file) + ', status=' + str(self.status) + ']'
