from django.http import HttpResponse
import simplejson

@require_GET
def full(request):
    response = HttpResponse(mimetype='application/json')
    simplejson.dump(data, request.GET)
    return response

@require_GET
def group(request):
    response = HttpResponse(mimetype='application/json')
    simplejson.dump(data, request.GET)
    return response

@require_GET
def trait(request):
    response = HttpResponse(mimetype='application/json')
    simplejson.dump(data, request.GET)
    return response

