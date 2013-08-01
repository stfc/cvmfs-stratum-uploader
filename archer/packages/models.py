import re
import os
import tarfile

from django.db import models
from django.conf import settings
from archer.projects.models import Project


class Package(models.Model):
    def __get_upload_path(self, filename):
        return os.path.join(settings.MEDIA_ROOT, ".%s" % self.project, filename).replace('/./', '/')

    class Status:
        """Enumeration for Package status"""
        new, uploaded, unpacking, deployed, cancelled, deleted, undeployed, error = range(8)

    __STATUSES = dict((value, name) for name, value in vars(Status).items() if not name.startswith('__'))

    project = models.ForeignKey(Project)
    file = models.FileField(upload_to=__get_upload_path, max_length=1024)
    status = models.IntegerField(
        choices=__STATUSES.items(),
        blank=False,
        null=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = (
            ('deploy_package', 'Deploy package'),
            ('remove_package', 'Remove package'),
        )

    def status_name(self):
        return Package.__STATUSES[self.status]

    def can_remove(self):
        return self.status in [Package.Status.deployed, Package.Status.undeployed, Package.Status.uploaded]

    def can_deploy(self):
        return self.status in [Package.Status.uploaded, Package.Status.undeployed, Package.Status.cancelled] \
            and (os.path.isfile(self.file.path) and tarfile.is_tarfile(self.file.path))

    def filepath(self):
        """
        Returns path to the file but hides the path to MEDIA directory.
        """
        return re.sub('^%s' % settings.MEDIA_ROOT, '', self.file.path)

    def filename(self):
        """
        Returns name of the file without full path.
        """
        replace = os.path.join(settings.MEDIA_ROOT, self.project.full_path()[1::]) + '/'
        return re.sub('^%s' % replace, '', self.file.path)

    def get_file_list(self):
        """
        Returns list of files in the tarfile.
        """
        path = self.file.path
        if not os.path.isfile(path):
            return None
        if not tarfile.is_tarfile(path):
            return None
        tar = tarfile.open(path)
        names = tar.getnames()
        return names

    def deploy(self, subdir='', force=False):
        """
        Unpacks the tar file at the project directory.
        Any previous content is deleted.

        Returns True if deployment succeeded.
        Raises IOError if file does not exist.
        Raises ValueError if file is not a tar file.
        """
        import tarfile

        if self.can_deploy or force:
            file_path = self.file.path
            if not os.path.isfile(file_path):
                self.status = Package.Status.error
                self.save()
                raise IOError('package file ' + file_path + ' does not exist')
            if not tarfile.is_tarfile(file_path):
                self.status = Package.Status.error
                self.save()
                raise ValueError('package file ' + file_path + ' is not tarball file')
            try:
                self.project.clear_dir(subdir)
                with tarfile.open(file_path) as tar:
                    self.status = Package.Status.unpacking
                    self.save()
                    tar.extractall(path=self.project.full_path())
                    self.status = Package.Status.deployed
                    self.save()
                    return True
            except (OSError, ValueError, IOError):
                self.status = Package.Status.error
                self.save()
                return False
        else:
            return False

    def remove(self):
        """
        Removes package file from MEDIA directory.
        """
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
