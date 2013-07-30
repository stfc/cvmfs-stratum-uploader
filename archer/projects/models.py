import os
import shutil
from django.db import models


class FileSystem(models.Model):
    mount_point = models.CharField(max_length=2000, null=False, blank=False, unique=True)

    def __unicode__(self):
        return self.mount_point


class Project(models.Model):
    file_system = models.ForeignKey(FileSystem, null=False)
    directory = models.CharField(max_length=200, null=False, blank=False)

    class Meta:
        unique_together = ('file_system', 'directory')
        permissions = (
            ('view_project', 'View project'),
            ('upload_package', 'Upload package'),
            ('deploy_package', 'Deploy package'),
        )

    def full_path(self):
        return os.path.join(self.file_system.mount_point, self.directory)

    def clear_dir(self):
        """
        Removes all files in project directory.
        """
        try:
            for root, dirs, files in os.walk(self.full_path()):
                for f in files:
                    os.unlink(os.path.join(root, f))
                for d in dirs:
                    shutil.rmtree(os.path.join(root, d))
            return True
        except IOError as e:
            print e
            return False

    def __unicode__(self):
        return self.full_path()
