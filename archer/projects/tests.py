from django.test import TestCase
from django.utils import unittest
from models import Project


class ProjectTestCase(TestCase):
    def setUp(self):
        pass

    def test_project_cannot_be_empty(self):
        pass
        # p = Project.objects.create(file_system=None, directory=None)
