import os

app_configuration = os.environ['DJANGO_CONFIGURATION']
if app_configuration == 'production':
    from production import *
elif app_configuration == 'dev':
    from dev import *
elif app_configuration == 'test':
    from test import *
elif app_configuration.startswith('ci_'):
    exec "from archer.settings.ci_%s import *" % app_configuration.split('ci_')[1]
else:
    raise ValueError('Incorrect DJANGO_CONFIGURATION=%s' % app_configuration)
