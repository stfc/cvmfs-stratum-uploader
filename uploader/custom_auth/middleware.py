from django.core.urlresolvers import reverse
from django.http import HttpResponsePermanentRedirect


class NoLoginAdminRedirectMiddleware:
    """
    This middleware forbids to access admin page for unauthorized but authenticated users.
    """
    def process_request(self, request):
        if request.META['PATH_INFO'].startswith('/admin'):
            if not request.user.is_authenticated() or not request.user.is_staff:
                return HttpResponsePermanentRedirect(reverse('index'))
