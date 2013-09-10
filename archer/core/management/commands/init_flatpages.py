from django.core.management.base import BaseCommand, CommandError
from django.contrib.flatpages.models import FlatPage, Site
from archer.settings.common import get_host_name


class Command(BaseCommand):
    args = '[domain]'
    help = 'initialize static pages like "Getting Started"'

    def handle(self, *args, **options):
        site = Site.objects.get()
        if args:
            if len(args) > 1:
                raise CommandError('Command accept at most one parameter.')
            site.domain = args[0]
            site.name = args[0]
        else:
            hostname = get_host_name()
            site.domain = hostname
            site.name = hostname
        site.save()

        try:
            page = FlatPage.objects.get(url='/getting-started/')
            page.sites = [site]
            page.save()
        except FlatPage.DoesNotExist:
            page = FlatPage(url='/getting-started/', title='Getting Started', registration_required=False)
            page.content = 'Go to admin panel to change welcome message!'
            page.save()
            page.sites = [site]
            page.save()
