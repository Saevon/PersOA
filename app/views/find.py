from django.views.decorators.http import require_GET

from app.constants.index import INDEX_DIR
from app.errors import PersOARequiredFieldError, PersOANotFound, PersOALeftoverField
from app.models.choice import BasicChoice, LinearChoice, SubChoice
from app.models.group import TraitGroup
from app.models.trait import BasicTrait, LinearTrait
from app.views.field import Field
from app.views.whitelist import Whitelist
from app.views.search import WhooshIndex
from app.views.sanitize import json_return, persoa_output

# Do any preparatory work before starting requests
WhooshIndex.get(INDEX_DIR)

############################################################
# Find Trait Group
############################################################
# profile_whitelist = (Whitelist()
#     .add(seed_field)
#     .add(num_field.default(1))

#     .include(['trait_desc', 'desc', 'details', 'trait'], 'choice_trait')
#     .include(['choice_desc', 'desc', 'details'], 'choice_desc')
#     .include(['choice_name', 'name'], 'choice_name')
# )

@require_GET
@json_return
@persoa_output
def trait_group(request):
    pass

############################################################
# Find Trait
############################################################
trait_whitelist = (Whitelist()
    .add(Field(['trait_name', 'name', 'trait'], 'trait_name')
        .default(None))
    .add(Field(['trait_desc', 'desc'], 'trait_desc').default(None))
    .add(Field(['trait_type', 'type'], 'trait_type').default(None))
    # .add(Field(['limit', 'max'], 'limit').default(1))

    .include(['trait_name','name'], 'trait_name')
    .include(['choice', 'choices'], 'choice')
    .include(['choice_name', 'name'], 'choice_name')
    .include(['choice_desc', 'desc', 'details'], 'choice_desc')
    .include(['group', 'group'], 'group')
    .include(['group_name', 'name'], 'group_name')
)
TRAIT_TYPES = {
    'scale': 'LinearTrait',
    'basic': 'BasicTrait',
}

@require_GET
@json_return
@persoa_output
def trait(request, output=None):
    # TODO add query
    whitelist = trait_whitelist.clear()
    # Translate the input
    args = whitelist.process(request.GET)

    # Check the input for any problems
    whitelist.leftover(PersOALeftoverField)
    output.error(whitelist.errors())

    # Prepare the input
    kwargs = {'limit': 1}
    for key in ['name', 'desc']:
        if not args['trait_' + key] is None:
            kwargs[key] = [args['trait_' + key]]
    if (not args['trait_type'] is None
            and TRAIT_TYPES.has_key(args['trait_type'])):
        kwargs['type'] = [TRAIT_TYPES[args['trait_type']]]

    if not (kwargs.has_key('name') or kwargs.has_key('desc') or kwargs.has_key('type')):
        # raise an error or something
        return

    # Find the Trait
    trait = None

    results = WhooshIndex.get(INDEX_DIR).search(**kwargs)
    if len(results):
        cls = WhooshIndex.CLASSES['index'][results[0]['type']]

        trait = (cls.objects
            .select_related()
            .get(id=results[0]['id'])
        )
    else:
        output.error(PersOANotFound())

    # Format the result
    print args['include']
    output.output(trait.details(args[Whitelist.INCLUDE_NAME]))


############################################################
# Find Choice
############################################################

@require_GET
@json_return
@persoa_output
def choice(request):
    pass
