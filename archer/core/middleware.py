from django.contrib.auth.middleware import RemoteUserMiddleware


class CustomHeaderMiddleware(RemoteUserMiddleware):
    header = 'SSL_CLIENT_S_DN'
