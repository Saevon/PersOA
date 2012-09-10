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
# Get Trait Group
############################################################
profile_whitelist = (Whitelist()
    .add(seed_field)
    .add(num_field.default(1))

    .include(['trait_desc', 'desc', 'details', 'trait'], 'choice_trait')
    .include(['choice_desc', 'desc', 'details'], 'choice_desc')
    .include(['choice_name', 'name'], 'choice_name')
)

@require_GET
@json_return
@persoa_output
def trait_groups(request):
    pass

############################################################
# Get Trait
############################################################
profile_whitelist = (Whitelist()
    .add(seed_field)
    .add(num_field.default(1))

    .include(['trait_desc', 'desc', 'details', 'trait'], 'choice_trait')
    .include(['choice_desc', 'desc', 'details'], 'choice_desc')
    .include(['choice_name', 'name'], 'choice_name')
)

@require_GET
@json_return
@persoa_output
def traits(request):
    pass

############################################################
# Get choice
############################################################
choice = (Whitelist()
    .add(seed_field)
    .add(num_field.default(1))

    .include(['trait_desc', 'desc', 'details', 'trait'], 'choice_trait')
    .include(['choice_desc', 'desc', 'details'], 'choice_desc')
    .include(['choice_name', 'name'], 'choice_name')
)
CHOICE_TYPES = ['basic', 'linear'];

@require_GET
@json_return
@persoa_output
def choices(request):
    whitelist = [field(*item) for item in [
        [
            'name',
            ['choice_name', 'name'],
            basestring,
            None,
        ],
        [
            'type',
            ['choice_type', 'type'],
            basestring,
            None,
            lambda val: (val in CHOICE_TYPES),
        ],
        [
            'trait',
            ['trait', 'trait_name'],
            basestring,
            None,
        ],
        IncludeField(['trait'])
    ]]

    params = extract(request.GET, whitelist)

    response = HttpResponse(mimetype='application/json')
    simplejson.dump(params, response)
    return response

