from django.views.decorators.http import require_GET
from django.http import HttpResponse
import simplejson

from app.models.trait import BasicTrait, LinearTrait
from app.views.whitelist import Whitelist
from app.views.field import Field

@require_GET
def full(request):
    response = HttpResponse(mimetype='application/json')
    simplejson.dump(request.GET, response)
    return response

@require_GET
def group(request):
    response = HttpResponse(mimetype='application/json')
    simplejson.dump(request.GET, response)
    return response

@require_GET
def trait(request):
    # Translate the input
    args = (Whitelist()
        .require(Field(['trait_name', 'trait'],'trait_name', basestring))
        .include(['trait_desc', 'desc'], 'trait_desc')
        .include(['choice_desc', 'desc'], 'choice_desc')
        .process(request.GET)
    )

    # Find the Trait

    # Generate a choice

    # Format
    generated = args

    response = HttpResponse(mimetype='application/json')
    simplejson.dump(generated, response)
    return response

