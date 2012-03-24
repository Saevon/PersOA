from django.views.decorators.http import require_GET
from django.http import HttpResponse
import simplejson

from persoa_main.helpers import extract, field

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
            ['choice_name', 'name'],
            'name',
            basestring,
            None,
        ],
        [
            ['choice_type', 'type'],
            'type',
            basestring,
            None,
            lambda val: (val in CHOICE_TYPES),
        ],
        [
            ['trait', 'trait_name'],
            'trait',
            basestring,
            None,
        ],
        [
            ['include'],
            'include',
            list,
            None,
            lambda val: (reduce(is_str, val, True)),
        ],
    ]]

    params = extract(request.GET, whitelist)

    response = HttpResponse(mimetype='application/json')
    simplejson.dump(params, response)
    return response

