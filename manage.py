#!/usr/bin/env python
# from django.core.management import execute_manager
import os, sys
from django.core.management import execute_from_command_line

try:
    import transportal.settings # Assumed to be in the same directory.
except ImportError:
    import sys
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
    sys.exit(1)


def run():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "transportal.settings")
    execute_from_command_line(sys.argv)
    # execute_manager(settings)


if __name__ == "__main__":
    run()
