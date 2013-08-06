import os
import shutil
import uuid
from django.utils.unittest import TestCase
from archer.projects.models import Project, FileSystem


class ProjectTestCase(TestCase):
    def setUp(self):
        uid = str(uuid.uuid4())[0:8]
        self.mount_point = ('/tmp/cvmfs-%s' % uid)
        self.fs = FileSystem.objects.create(mount_point=self.mount_point)
        os.makedirs(self.fs.mount_point)

        # def remove_mount_point():
        #     os.chmod(self.fs.mount_point, 02700)
        #     shutil.rmtree(self.fs.mount_point)
        # self.addCleanup(remove_mount_point())

        self.project1 = Project(file_system=self.fs, directory='project1')

    def test_full_path(self):
        project2 = Project(file_system=self.fs, directory='project2')
        self.assertEqual(project2.full_path(), os.path.join(self.fs.mount_point, 'project2'))

    def test_clear_dir(self):
        directory = os.path.join(self.fs.mount_point, 'project2')
        if not os.path.exists(directory):
            os.makedirs(directory)

        project2 = Project(file_system=self.fs, directory='project2')

        try:
            project2.clear_dir()
        except (IOError, OSError, ValueError) as e:
            print(e)
            self.fail(e)

    def test_clear_dir_no_dir(self):
        directory = os.path.join(self.fs.mount_point, 'project2')
        if os.path.exists(directory):
            shutil.rmtree(directory)

        with self.assertRaises(ValueError):
            p = Project(file_system=self.fs, directory='project2')
            p.clear_dir()

    def test_clear_dir_no_chmod(self):
        directory = os.path.join(self.fs.mount_point, 'project2')
        if not os.path.exists(directory):
            os.makedirs(directory)
        os.mkdir(os.path.join(directory, 'something'))
        os.chmod(directory, 02400)

        with self.assertRaises(OSError):
            p = Project(file_system=self.fs, directory='project2')
            p.clear_dir()

    def test_clear_dir_no_mount_point_chmod(self):
        directory = os.path.join(self.fs.mount_point, 'project2')
        if not os.path.exists(directory):
            os.makedirs(directory)
        os.mkdir(os.path.join(directory, 'something'))
        os.chmod(self.fs.mount_point, 02444)

        with self.assertRaises(ValueError):
            p = Project(file_system=self.fs, directory='project2')
            p.clear_dir()

    def test_subdir_none_or_empty(self):
        should_be = '%s/%s' % (self.mount_point, self.project1.directory)

        dir1 = self.project1.subdir()
        dir2 = self.project1.subdir('')
        dir3 = self.project1.subdir('.')
        dir4 = self.project1.subdir('././.')

        self.assertEqual(os.path.realpath(dir1), should_be)
        self.assertEqual(os.path.realpath(dir2), should_be)
        self.assertEqual(os.path.realpath(dir3), should_be)
