from django.views.decorators.http import require_GET
from django.http import HttpResponse
import simplejson

from app.constants.index import INDEX_DIR
from app.errors import PersOARequiredFieldError, PersOANotFound, PersOALeftoverField
from app.models.trait import BasicTrait, LinearTrait
from app.views.field import Field
from app.views.whitelist import Whitelist
from app.views.search import WhooshIndex
from app.views.sanitize import json_return, persoa_output
from itertools import chain

WhooshIndex.get(INDEX_DIR)

seed_field = Field(['seed'],'seed', int).default(None)
num_field = Field(['num'], 'num', int).default(None)

############################################################
# Generate Full
############################################################
full_whitelist = (Whitelist()
    .add(seed_field)
    .add(num_field.default(1))

    .include(['trait_desc', 'desc', 'details', 'trait'], 'choice_trait')
    .include(['choice_desc', 'desc', 'details'], 'choice_desc')
    .include(['choice_name', 'name'], 'choice_name')
)

@require_GET
@json_return
@persoa_output
def full(request, output=None):
    whitelist = full_whitelist.clear()
    # Translate the input
    args = whitelist.process(request.GET)

    # Check the input for any problems
    whitelist.leftover(PersOALeftoverField)
    output.error(whitelist.errors())

    # Generate each trait
    generated = []
    for i in range(args['num']):
        profile = {}
        traits = chain(BasicTrait.objects.all(), LinearTrait.objects.all())
        for trait in traits:
            profile[trait.name] = [
                i.details(args[Whitelist.INCLUDE_NAME])
                for i in trait.generate(seed=args['seed'])
            ]
        generated.append(profile)

    # Format the choice
    output.output(generated)

############################################################
# Generate Group
############################################################
group_whitelist = (Whitelist()
    .add(Field(['group_name', 'group', 'name'],'group_name', basestring)
        .default(PersOARequiredFieldError))
    .add(seed_field)
    .add(num_field)

    .include(['group_desc', 'desc', 'details'], 'group_desc')
    .include(['trait_desc', 'desc', 'details', 'trait'], 'choice_trait')
    .include(['choice_desc', 'desc', 'details'], 'choice_desc')
    .include(['choice_name', 'name'], 'choice_name')
)

@require_GET
@json_return
@persoa_output
def group(request, output=None):
    whitelist = group_whitelist.clear()
    # Translate the input
    args = whitelist.process(request.GET)

    # Check the input for any problems
    whitelist.leftover(PersOALeftoverField)
    output.error(whitelist.errors())

    # Find the Group
    group = None

    results = WhooshIndex.get(INDEX_DIR).search(
        name=[args['group_name']],
        type=WhooshIndex.CLASSES['group']
    )
    if len(results):
        cls = WhooshIndex.CLASSES['index'][results[0]['type']]

        group = (cls.objects
            .select_related()
            .get(id=results[0]['id'])
        )
    else:
        output.error(PersOANotFound())

    # Generate a choice
    output.output(group.generate(
        args['num'],
        args['seed'],
        args[Whitelist.INCLUDE_NAME]
    ))


############################################################
# Generate Trait
############################################################
trait_whitelist = (Whitelist()
    .add(Field(['trait_name', 'trait', 'name'],'trait_name', basestring).default(PersOARequiredFieldError))
    .add(seed_field)
    .add(num_field)

    .include(['trait_desc', 'desc', 'details', 'trait'], 'choice_trait')
    .include(['choice_desc', 'desc', 'details'], 'choice_desc')
    .include(['choice_name', 'name'], 'choice_name')
)

@require_GET
@json_return
@persoa_output
def trait(request, output=None):
    whitelist = trait_whitelist.clear()
    # Translate the input
    args = whitelist.process(request.GET)

    # Check the input for anyproblems
    whitelist.leftover(PersOALeftoverField)
    output.error(whitelist.errors())

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
        output.error(PersOANotFound())

    # Generate a choice
    generated = trait.generate(num=args['num'], seed=args['seed'])
    # Format the choice
    output.output(
        [i.details(args[Whitelist.INCLUDE_NAME])
        for i in generated]
    )

