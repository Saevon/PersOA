from django.views.decorators.http import require_GET
from django.http import HttpResponse
import simplejson

@require_GET
def index(request):
    response = HttpResponse(mimetype='application/json')
    simplejson.dump(request.GET, response)
    return response

@require_GET
def about(request):
    out = {
        'authors': ['Saevon', 'BlastOfWind'],
        'created': 'December 15th 2011',
        'desc': 'An app that is used to generate, view or store roleplaying personalities. Based on AshAmi\'s personality site',
        'links': ['http://rpg.ashami.com/'],
    }
    response = HttpResponse(mimetype='application/json')
    simplejson.dump(out, response)
    return response
