import os
from pprint import pprint
import shutil
from django.conf import settings
from django.contrib.auth.models import User, Group
from django.db import models


class FileSystem(models.Model):
    mount_point = models.CharField(max_length=2000, null=False, blank=False, unique=True)

    def __unicode__(self):
        return self.mount_point


class Project(models.Model):
    file_system = models.ForeignKey(FileSystem)
    directory = models.CharField(max_length=200, null=False, blank=False)
    group = models.ForeignKey(Group, null=True, blank=True, unique=True)

    class Meta:
        unique_together = ('file_system', 'directory')

    def full_path(self):
        return os.path.join(self.file_system.mount_point, self.directory)

    def __unicode__(self):
        return self.full_path()
        # return os.path.join(str(self.file_system), str(self.directory))


class Package(models.Model):
    def __get_upload_path(instance, filename):
        return os.path.join(settings.MEDIA_ROOT, ".%s" % instance.project, filename).replace('/./', '/')

    class Status:
        new, uploaded, unpacking, deployed, cancelled, deleted, undeployed = range(7)

    __STATUSES = dict((value, name) for name, value in vars(Status).items() if not name.startswith('__'))

    project = models.ForeignKey(Project)
    file = models.FileField(upload_to=__get_upload_path)
    status = models.IntegerField(
        choices=__STATUSES.items(),
        blank=False,
        null=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def status_name(self):
        return Package.__STATUSES[self.status]

    def can_remove(self):
        return self.status in [Package.Status.deployed, Package.Status.undeployed, Package.Status.uploaded]

    def can_deploy(self):
        return self.status in [Package.Status.uploaded, Package.Status.undeployed, Package.Status.cancelled]


    @staticmethod
    def clear_dir(dir):
        try:
            for root, dirs, files in os.walk(dir):
                for f in files:
                    os.unlink(os.path.join(root, f))
                for d in dirs:
                    shutil.rmtree(os.path.join(root, d))
        except IOError as e:
            print e
            return False

    def deploy(self, force=False):
        import tarfile

        if self.can_deploy or force:
            if not os.path.isfile(self.file.path):
                raise IOError('package file ' + self.file.path + ' does not exist')
            self.status = Package.Status.unpacking
            self.save()
            Package.clear_dir(self.project.full_path())
            if not tarfile.is_tarfile(self.file.path):
                raise IOError('package file ' + self.file.path + ' is not tarball file')
            path = self.file.path
            tar = tarfile.open(path)
            # tar.list()
            tar.extractall(path=self.project.full_path())
            tar.close()
            self.status = Package.Status.deployed
            self.save()
            return True
        else:
            return False

    def remove(self):
        result = False
        if os.path.isfile(self.file.path):
            os.unlink(self.file.path)
            result = True
        self.status = Package.Status.deleted
        self.save()
        return result


    def __unicode__(self):
        return 'Package[project=' + str(self.project) + ', file=' + str(self.file) + ', status=' + Package.__STATUSES[
            self.status] + ']'
