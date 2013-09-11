import django.contrib.auth.backends


class RemoteUserBackend(django.contrib.auth.backends.RemoteUserBackend):
    create_unknown_user = False
