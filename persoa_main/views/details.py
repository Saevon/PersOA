from django.views.decorators.http import require_GET
from django.http import HttpResponse
import simplejson

from helpers.decorators import cascade
from app.helpers import extract, field, IncludeField

@require_GET
def trait_groups(request):
    response = HttpResponse(mimetype='application/json')
    simplejson.dump(request.GET, response)
    return response

@require_GET
def traits(request):
    response = HttpResponse(mimetype='application/json')
    simplejson.dump(request.GET, response)
    return response

CHOICE_TYPES = ['basic', 'linear'];

def is_str(other, val):
    return isinstance(val, basestring) and other

@require_GET
def choices(request):
    whitelist = [field(*item) for item in [
        [
            'name',
            ['choice_name', 'name'],
            basestring,
            None,
        ],
        [
            'type',
            ['choice_type', 'type'],
            basestring,
            None,
            lambda val: (val in CHOICE_TYPES),
        ],
        [
            'trait',
            ['trait', 'trait_name'],
            basestring,
            None,
        ],
        IncludeField(['trait'])
    ]]

    params = extract(request.GET, whitelist)

    response = HttpResponse(mimetype='application/json')
    simplejson.dump(params, response)
    return response

