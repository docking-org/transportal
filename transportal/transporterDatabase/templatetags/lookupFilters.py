from django import template
from transportal.transporterDatabase.models import Expression

register = template.Library()
def keyConvStr(d, key_name):
    try:
        value = d[str(key_name)]
    except KeyError:
        from django.conf import settings

        value = 'Lookup failed ' + str(key_name)

    return value
key = register.filter('keyConvStr', keyConvStr)
