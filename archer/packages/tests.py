import os
import uuid
import shutil
from django.utils.unittest import TestCase
from archer.projects.models import FileSystem, Project
from archer.packages.models import Package
from archer import settings


class PackageTestCase(TestCase):
    def setUp(self):
        uid = str(uuid.uuid4())[0:8]
        self.fs = FileSystem.objects.create(mount_point=('/tmp/cvmfs-%s' % uid))
        self.project = Project(file_system=self.fs, directory='project')
        os.makedirs(self.fs.mount_point)
        settings.MEDIA_ROOT = '/tmp/media-%s' % uid
        os.makedirs(settings.MEDIA_ROOT)

        self.filepath = '%s/package.tar.gz' % settings.MEDIA_ROOT
        open(self.filepath, 'w').close()

    def test_new_after_init(self):
        package = Package(project=self.project, file=self.filepath)

        self.assertEqual(package.status, Package.Status.new)

    def test_filepath(self):
        pass
        # file = open(os.path.join(self.project.full_path(), 'filename.tar.gz'), 'w')
        # file.close()
        #
        # p = Package(project=self.project, file=file)
        #
        # self.assertEqual(p.filepath(), os.path.join())

    def test_filename(self):
        pass

    def test_get_file_list(self):
        pass

    def test_deploy(self):
        pass

    def test_remove(self):
        pass

    def tearDown(self):
        shutil.rmtree(settings.MEDIA_ROOT)