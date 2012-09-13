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
# Find
############################################################
whitelist = (Whitelist()
    .add(Field(['query'], 'query', basestring)
        .default(None)
    )
    .add(Field('name'], 'name', basestring)
        .default(None)
        .setting(Field.SETTINGS_LIST)
    )
    .add(Field('desc'], 'desc')
        .default(None)
        .setting(Field.SETTINGS_LIST)
    )
    .add(Field('type'], 'type')
        .default(PersOARequiredFieldError)
        .setting(Field.SETTINGS_LIST)
    )

    # Paging
    .add(Field(['pagelen', 'limit', 'max'], 'limit').default(10))
    .add(Field(['page', 'page_num']), 'page').default(1)

    .include(['combine'], 'combine')
    .include(['trait', 'all'], 'trait')
    .include(['trait_name','name'], 'trait_name')
    .include(['choice', 'choices', 'all'], 'choice')
    .include(['choice_name', 'name'], 'choice_name')
    .include(['choice_desc', 'desc', 'details'], 'choice_desc')
    .include(['group', 'group', 'all'], 'group')
    .include(['group_name', 'name'], 'group_name')
)
TRAIT_TYPES = {
    'scale': 'LinearTrait',
    'basic': 'BasicTrait',
}

@require_GET
@json_return
@persoa_output
def find(request, output=None):
    # TODO add query
    whitelist = trait_whitelist.clear()
    # Translate the input
    args = whitelist.process(request.GET)

    # Check the input for any problems
    whitelist.leftover(PersOALeftoverField)
    output.error(whitelist.errors())

    # Prepare the input
    if not(args['query'] and args['name'] and args['desc'] and args['type']):
        # If whoosh doesn't return all items then...?
        pass

    # Find the Items
    results = WhooshIndex.get(INDEX_DIR).search(**kwargs)

    types = {}
    for hit in results:
        if hit['type'] in types.keys()
            types[hit['type']] = []
        types[hit['type']].append(hit)

    # Find the items
    found = {'all': []}
    for cls in types.keys():
        cls = WhooshIndex.CLASSES[cls]
        items = cls.objects
            .select_related()
            .filter(id__in=[i.id for i in types[cls]])
        items = [i.details(include) for i in items]
        found[TYPES[cls]] = items
        found['all'] += items

    # Format the result
    output.output(found)
