from django.views import debug
from django.conf import settings as conf_settings

EXPOSED_SETTINGS = getattr(conf_settings, 'EXPOSED_SETTINGS', None)


def settings(request):
    exposed = {}
    if EXPOSED_SETTINGS:
        for x in EXPOSED_SETTINGS:
            exposed[x] = getattr(conf_settings, x)
    return { 'settings': exposed }


def module_view(request):
    return {'module_name': getattr(request, 'module_name', '').replace('.','-'),
            'view_name'  : getattr(request, 'view_name', '').replace('.','-')} 
