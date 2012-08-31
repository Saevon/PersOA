from django.views.decorators.http import require_GET
from django.http import HttpResponse
import simplejson

@require_GET
def index(request):
    response = HttpResponse(mimetype='application/json')
    simplejson.dump(request, response.GET)
    return response

@require_GET
def about(request):
    response = HttpResponse(mimetype='application/json')
    simplejson.dump(request, response.GET)
    return response
