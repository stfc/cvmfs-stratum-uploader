from django.db import models

# Create your models here.

# class User(models.Model):
#     name = models.CharField(max_length=200, null=False)
#     cert = models.CharField(max_length=1000)
#
#     def __unicode__(self):
#         return 'User[name=' + str(self.name) + ', cert=' + str(self.cert) + ']'


class CvmFs(models.Model):
    mount_point = models.CharField(max_length=2000, null=False, unique=True)

    def __unicode__(self):
        return self.mount_point


class Package(models.Model):
    fs = models.ForeignKey(CvmFs)
    file_path = models.FilePathField(path='/', allow_files=True, allow_folders=False, null=True)

    def __unicode__(self):
        return 'Package[fs=' + str(self.fs) + ', file_path=' + self.file_path + ']'

