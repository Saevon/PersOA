from django.views.decorators.http import require_GET

from app.constants import VERSION
from app.views.sanitize import json_return, persoa_output

@require_GET
@json_return
@persoa_output
def index(request, output=None):
    out = {
        'desc': 'Welcome to PersOA, an app dedicated to working with personalities.',
    }
    output.output(out)

@require_GET
@json_return
@persoa_output
def about(request, output=None):
    out = {
        'authors': ['Saevon', 'BlastOfWind'],
        'version': VERSION,
        'created': 'December 15th 2011',
        'desc': 'An app that is used to generate, view or store roleplaying personalities. Based on AshAmi\'s personality site',
        'links': ['http://rpg.ashami.com/'],
    }
    output.output(out)
