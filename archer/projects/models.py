import os
import shutil
from django.db import models


class FileSystem(models.Model):
    alias = models.CharField(max_length=2000, blank=True)
    mount_point = models.CharField(max_length=2000, null=False, blank=False, unique=True)

    def alias_path(self):
        if self.alias is None or len(self.alias) == 0:
            return self.mount_point
        else:
            return self.alias

    def __unicode__(self):
        return self.alias_path()


class Project(models.Model):
    file_system = models.ForeignKey(FileSystem, null=False)
    directory = models.CharField(max_length=200, null=False, blank=False)

    class Meta:
        unique_together = ('file_system', 'directory')
        permissions = (
            ('view_project', 'View project'),
            ('upload_package', 'Upload package'),
            ('deploy_package', 'Deploy package'),
            ('make_directory', 'Make directory'),
            ('remove_directory', 'Remove directory'),
        )

    def full_path(self):
        return os.path.join(self.file_system.mount_point, self.directory)

    def alias_path(self):
        return os.path.join(self.file_system.alias_path(), self.directory)

    def subdir(self, subdir=''):
        """
        Returns absolute path to subdirectory of `self.directory`.
        Raises ValueError if `subdir` is not a offspring of `self.directory`.
        """
        if subdir is None or len(subdir) == 0:
            return self.full_path()
        if subdir.startswith('/'):
            raise ValueError('Cannot provide root path "%s" as subdir!' % subdir)
        if os.path.relpath(subdir).startswith('..'):
            raise ValueError('')
        return os.path.abspath(os.path.join(self.full_path(), subdir))

    def clear_dir(self, subdir=''):
        """
        Removes all files in project's directory.
        """
        if not os.path.isdir(self.file_system.mount_point):
            raise ValueError("mount_point %s is not a directory" % self.file_system.mount_point)
        if not os.path.isdir(self.full_path()):
            raise ValueError("project %s is not a directory" % self.full_path())
        path = self.subdir(subdir)
        if not os.path.isdir(path):
            raise ValueError("%s is not a directory" % path)
        for root, dirs, files in os.walk(path):
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))
        return True

    def __unicode__(self):
        return self.alias_path()
