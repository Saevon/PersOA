from django.views.decorators.http import require_GET
from django.http import HttpResponse
import simplejson

from app.models.trait import BasicTrait, LinearTrait
from app.views.field import Field
from app.views.whitelist import Whitelist

@require_GET
def full(request):
    args = (Whitelist()
        .add(Field(['seed'],'seed', int))
        .add(Field(['num'], 'num', int))
        .include(['trait_desc', 'desc', 'details'], 'trait_desc')
        .include(['choice_desc', 'desc', 'details'], 'choice_desc')
    ).process(request.GET)

    # Find the Group

    # Generate the group

    # Format
    generated = args

    response = HttpResponse(mimetype='application/json')
    simplejson.dump(generated, response)
    return response

@require_GET
def group(request):
    args = (Whitelist()
        .add(Field(['group_name', 'group', 'name'],'group_name', basestring))
        .add(Field(['seed'],'seed', int))
        .add(Field(['num'], 'num', int))
        .include(['group_desc', 'desc', 'details'], 'group_desc')
        .include(['trait_desc', 'desc', 'details'], 'trait_desc')
        .include(['choice_desc', 'desc', 'details'], 'choice_desc')
    ).process(request.GET)

    # Find the Group

    # Generate the group

    # Format
    generated = args

    response = HttpResponse(mimetype='application/json')
    simplejson.dump(generated, response)
    return response

@require_GET
def trait(request):
    # Translate the input
    args = (Whitelist()
        .add(Field(['trait_name', 'trait', 'name'],'trait_name', basestring))
        .add(Field(['seed'],'seed', int).default(None))
        .add(Field(['num'], 'num', int).default(None))
        .include(['trait_desc', 'desc', 'details'], 'trait_desc')
        .include(['choice_desc', 'desc', 'details'], 'choice_desc')
    ).process(request.GET)

    # Find the Trait
    # Temporarily hard-coded
    trait = (BasicTrait.objects
        .select_related()
        .get(name='Primary Motivator')
    )

    # Generate a choice
    if args['seed'] == None:
        generated = trait.generate(args['num'])
    generated = trait.generate(args['num'] ,args['seed'])

    # Format
    # generated = trait.details()

    response = HttpResponse(mimetype='application/json')
    simplejson.dump(generated, response)
    return response

