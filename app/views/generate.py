from django.views.decorators.http import require_GET
from django.http import HttpResponse
import simplejson

from app.constants.index import INDEX_DIR
from app.errors import persoa_errors, PersOARequiredFieldError
from app.models.trait import BasicTrait, LinearTrait
from app.views.field import Field
from app.views.whitelist import Whitelist
from app.views.search import WhooshIndex
from utils.decorators import json_return

WhooshIndex.get(INDEX_DIR)

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
@json_return
def trait(request):
    # Translate the input
    whitelist = (Whitelist()
        .add(Field(['trait_name', 'trait', 'name'],'trait_name', basestring).default(PersOARequiredFieldError))
        .add(Field(['seed'],'seed', int).default(None))
        .add(Field(['num'], 'num', int).default(None))
        .include(['trait_desc', 'desc', 'details', 'trait'], 'choice_trait')
        .include(['choice_desc', 'desc', 'details'], 'choice_desc')
        .include(['choice_name', 'name'], 'choice_name')
    )
    args = whitelist.process(request.GET)

    # Check the input for any problems
    errors = whitelist.errors()
    whitelist.clear_errors()

    if len(errors):
        return persoa_errors(errors)

    # Find the Trait
    trait = None

    results = WhooshIndex.get(INDEX_DIR).search(
        name=[args['trait_name']],
        type=WhooshIndex.CLASSES['trait']
    )
    if len(results):
        cls = WhooshIndex.CLASSES['index'][results[0]['type']]

        trait = (cls.objects
            .select_related()
            .get(id=results[0]['id'])
        )
    else:
        name = args['trait_name']
        try:
            trait = (BasicTrait.objects
                .select_related()
                .get(name=name)
            )
        except BasicTrait.DoesNotExist:
            trait = (LinearTrait.objects
                .select_related()
                .get(name=name)
            )

    # Generate a choice
    generated = trait.generate(args['num'], args['seed'])
    generated = [i.details(args[Whitelist.INCLUDE_NAME]) for
        i in generated]

    # Format
    # generated = trait.details()

    return generated

