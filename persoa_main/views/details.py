from django.views.decorators.http import require_GET
from django.http import HttpResponse
import simplejson

@require_GET
def trait_groups(request):
    response = HttpResponse(mimetype='application/json')
    simplejson.dump(data, request.GET)
    return response

@require_GET
def traits(request):
    response = HttpResponse(mimetype='application/json')
    simplejson.dump(data, request.GET)
    return response

@require_GET
def choices(request):
    response = HttpResponse(mimetype='application/json')
    data = {'a':request.GET}
    simplejson.dump(data, request.GET)
    return response

