from django.views.decorators.http import require_GET

from app.constants.index import INDEX_DIR
from app.errors import PersOARequiredFieldError, PersOANotFound, PersOALeftoverField
from app.models.trait import BasicTrait, LinearTrait
from app.views.field import Field
from app.views.whitelist import Whitelist
from app.views.search import WhooshIndex
from app.views.sanitize import json_return, persoa_output
from itertools import chain

# Do any preparatory work before starting requests
WhooshIndex.get(INDEX_DIR)

seed_field = Field(['seed'],'seed', int).default(None)
num_field = Field(['num'], 'num', int).default(None)


############################################################
# Generate Profile
############################################################
profile_whitelist = (Whitelist()
    .add(seed_field)
    .add(num_field.default(1))

    .include(['trait', 'desc', 'details'], 'trait')
    .include(['trait_name', 'name'], 'trait_name')
    .include(['choice_name', 'name'], 'choice_name')
    .include(['choice_desc', 'desc', 'details'], 'choice_desc')
)

@require_GET
@json_return
@persoa_output
def profile(request, output=None):
    whitelist = profile_whitelist.clear()
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

    .include(['group', 'group_name'], 'group')
    .include(['group_name', 'name'], 'group_name')
    .include(['trait'], 'trait')
    .include(['trait_name', 'name'], 'trait_name')
    .include(['choice_name', 'name'], 'choice_name')
    .include(['choice_desc', 'desc', 'details'], 'choice_desc')
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
        type=WhooshIndex.CLASSES['group'],
        page=1,
        pagelen=1
    )
    if len(results):
        cls = WhooshIndex.CLASSES['index'][results['results'][0]['type']]

        group = (cls.objects
            .select_related()
            .get(id=results['results'][0]['id'])
        )
    else:
        output.error(PersOANotFound())

    # Generate a choice
    include = args[Whitelist.INCLUDE_NAME]
    generated = {
        'choices': group.generate(
            args['num'],
            args['seed'],
            include
    )}
    if include['group']:
        generated['group'] = group.details(include)
    output.output(generated)


############################################################
# Generate Trait
############################################################
trait_whitelist = (Whitelist()
    .add(Field(['trait_name', 'trait', 'name'],'trait_name', basestring).default(PersOARequiredFieldError))
    .add(seed_field)
    .add(num_field)

    .include(['choice_desc', 'desc', 'details'], 'choice_desc')
    .include(['choice_name', 'name'], 'choice_name')
    .include(['trait', 'trait_name'], 'trait')
    .include(['trait_name', 'name'], 'trait_name')
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
        type=WhooshIndex.CLASSES['trait'],
        page=1,
        pagelen=1
    )
    if len(results):
        cls = WhooshIndex.CLASSES['index'][results[0]['type']]

        trait = (cls.objects
            .select_related()
            .get(id=results['results'][0]['id'])
        )
    else:
        output.error(PersOANotFound())

    # Generate a choice
    include = args[Whitelist.INCLUDE_NAME]
    generated = {
        'choices': [
            i.details(include)
            for i in trait.generate(num=args['num'], seed=args['seed'])
        ],
    }
    if include['trait']:
        generated['trait'] = trait.details(include)
    # Format the choice
    output.output(generated)
