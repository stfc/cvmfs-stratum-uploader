"""
Management utility to create admin with DN as username.
"""
from __future__ import unicode_literals

from pprint import pprint
import sys
from optparse import make_option

from django.core import exceptions
from django.core.management.base import BaseCommand, CommandError
from django.db import DEFAULT_DB_ALIAS
from uploader.custom_auth.models import User


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        # Options are defined in an __init__ method to support swapping out
        # custom user models in tests.
        super(Command, self).__init__(*args, **kwargs)
        self.UserModel = User
        self.username_field = self.UserModel._meta.get_field('username')

        self.option_list = BaseCommand.option_list + (
            make_option('--dn', dest='CERTIFICATE_DN', default=None,
                        help='Specifies the DN for the admin.'),
            make_option('--database', action='store', dest='database',
                        default=DEFAULT_DB_ALIAS, help='Specifies the database to use. Default is "default".'),
        )

    option_list = BaseCommand.option_list
    help = 'Used to create a admin.'

    def handle(self, *args, **options):
        username = options.get('CERTIFICATE_DN', None)
        interactive = username is None
        verbosity = int(options.get('verbosity', 1))
        database = options.get('database')

        user_data = {}

        if not interactive:
            try:
                username = self.username_field.clean(username, None)
            except exceptions.ValidationError as e:
                raise CommandError('; '.join(e.messages))
        else:
            # Prompt for DN
            # Enclose this whole thing in a try/except to trap for a
            # keyboard interrupt and exit gracefully.
            try:

                # Get a username
                while username is None:
                    raw_value = ''
                    if not username:
                        raw_value = raw_input('DN: ')
                    try:
                        username = self.username_field.clean(raw_value, None)
                    except exceptions.ValidationError as e:
                        self.stderr.write("Error: %s" % '; '.join(e.messages))
                        username = None
                        continue
                    try:
                        self.UserModel._default_manager.db_manager(database).get_by_natural_key(username)
                    except self.UserModel.DoesNotExist:
                        pass
                    else:
                        self.stderr.write("Error: That DN is already taken.")
                        username = None

            except KeyboardInterrupt:
                self.stderr.write("\nOperation cancelled.")
                sys.exit(1)
        pprint(username)
        user_data['dn'] = username

        self.UserModel._default_manager.db_manager(database).create_superuser(user_data['dn'], None, None)

        if verbosity >= 1:
            self.stdout.write("Superuser created successfully.")