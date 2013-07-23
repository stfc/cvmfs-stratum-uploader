import os
import sys

sys.path = ['/home/vwa13376/workspace/archer'] + sys.path

os.environ['DJANGO_SETTINGS_MODULE'] = 'archer.settings'


import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()


from django.contrib.auth.handlers.modwsgi import check_password

#def check_password(environ, username, password):
#    import django.contrib.auth.handlers.modwsgi
#    return django.contrib.auth.handlers.modwsgi.check_password(environ, username, password)
