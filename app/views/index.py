from django.views.decorators.http import require_GET
from django.http import HttpResponse

from app.views.sanitize import json_return, persoa_output
import simplejson

@require_GET
@json_return
@persoa_output
def index(request, output=None):
    pass

@require_GET
@json_return
@persoa_output
def about(request, output=None):
    out = {
        'authors': ['Saevon', 'BlastOfWind'],
        'created': 'December 15th 2011',
        'desc': 'An app that is used to generate, view or store roleplaying personalities. Based on AshAmi\'s personality site',
        'links': ['http://rpg.ashami.com/'],
    }
    output.output(out)
