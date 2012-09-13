from django.views.decorators.http import require_GET

from app.constants.index import INDEX_DIR, ALL_TYPES
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
    .add(Field(['name'], 'name', basestring)
        .default(None)
        .setting(Field.SETTINGS_LIST)
    )
    .add(Field(['desc'], 'desc', basestring)
        .default(None)
        .setting(Field.SETTINGS_LIST)
    )
    .add(Field(['type'], 'type', basestring)
        .default(PersOARequiredFieldError)
        .setting(Field.SETTINGS_LIST)
    )

    # Paging
    .add(Field(['pagelen', 'limit', 'max'], 'limit').default(10))
    .add(Field(['page', 'page_num'], 'page').default(1))

    .include(['combine'], 'combine')
    .include(['trait', 'all'], 'trait')
    .include(['trait_name','name'], 'trait_name')
    .include(['choice', 'choices', 'all'], 'choice')
    .include(['choice_name', 'name'], 'choice_name')
    .include(['choice_desc', 'desc', 'details'], 'choice_desc')
    .include(['group', 'group', 'all'], 'group')
    .include(['group_name', 'name'], 'group_name')
)

@require_GET
@json_return
@persoa_output
def find(request, output=None):
    # TODO add query
    whitelist.clear()
    # Translate the input
    kwargs = whitelist.process(request.GET)

    # Check the input for any problems
    whitelist.leftover(PersOALeftoverField)
    output.error(whitelist.errors())

    # Prepare the input
    if not(kwargs['query'] and kwargs['name'] and kwargs['desc'] and kwargs['type']):
        # If whoosh doesn't return all items then...?
        pass

    if not kwargs['type'] is None:
        types = kwargs['type']
        kwargs['type'] = set()
        for t in types:
            if t == 'all':
                kwargs['type'] = ALL_TYPES.values()
                break
            elif t in ALL_TYPES.keys():
                kwargs['type'].add(ALL_TYPES[t])
            elif t == 'trait':
                kwargs['type'] = args['type'] | WhooshIndex.CLASSES['trait']
            elif t == 'choice':
                kwargs['type'] = args['type'] | WhooshIndex.CLASSES['choice']

    # Find the Items
    results = WhooshIndex.get(INDEX_DIR).search(**kwargs)

    types = {}
    for hit in results['results']:
        if not hit['type'] in types.keys():
            types[hit['type']] = []
        types[hit['type']].append(hit)

    # Get the items from the database and format them
    include = kwargs[Whitelist.INCLUDE_NAME]
    print include
    found = {'all': []}
    for cls in types.keys():
        items = (WhooshIndex.CLASSES['index'][cls].objects
            .select_related()
            .filter(id__in=[i['id'] for i in types[cls]])
        )
        items = [i.details(include) for i in items]

        # TODO: properly name this
        found[cls] = items
        found['all'] += items

    if include['combine']:
        found.pop('all')

    # Format the result
    found['page'] = results['page']
    found['pages'] = results['pages']
    found['total'] = results['total']
    output.output(found)
