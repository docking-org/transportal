import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'fdadjango.settings'

sys.path.insert(0, '/home/btsadmin/public_html/chrisw/fda/fdadjango')
sys.path.insert(0, '/home/btsadmin/public_html/chrisw/fda')

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
