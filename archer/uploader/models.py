from django.db import models

# Create your models here.

# class User(models.Model):
#     name = models.CharField(max_length=200, null=False)
#     cert = models.CharField(max_length=1000)
#
#     def __unicode__(self):
#         return 'User[name=' + str(self.name) + ', cert=' + str(self.cert) + ']'


class CvmFs(models.Model):
    mount_point = models.CharField(max_length=2000, null=False, blank=False, unique=True)

    def __unicode__(self):
        return self.mount_point

class Package(models.Model):
    def get_upload_path(instance, filename):
        import os
        return os.path.join('uploads', ".%s" % instance.fs, filename)
    STATUSES = [(a, a) for a in ['new', 'uploaded', 'unpacking', 'deployed', 'cancelled', 'deleted']]
    STATUSES_LENGTH = 10 # max(STATUSES, key=len)
    fs = models.ForeignKey(CvmFs)
    file = models.FileField(upload_to=get_upload_path, )
    status = models.CharField(max_length=STATUSES_LENGTH, choices=STATUSES, blank=False, null=False)

    def __unicode__(self):
        return 'Package[fs=' + str(self.fs) + ', file=' + str(self.file) + ', status=' + str(self.status) + ']'


class Tarball(models.Model):
    from multiuploader.forms import MultiuploaderField

    name = models.CharField(max_length=2000, null=False, blank=False, unique=True)
    files = MultiuploaderField(required=False)

    def __unicode__(self):
        return str(self.name) + ' ' + str(self.files)