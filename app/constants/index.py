# Index related options
INDEX_DIR = 'index/'

TRAIT_TYPES = {
    'scale_trait': u'LinearTrait',
    'basic_trait': u'BasicTrait',
}

CHOICE_TYPES = {
    'sub_choice': u'SubChoice',
    'basic_choice': u'BasicChoice',
    'scale_choice': u'LinearChoice',
}

GROUP_TYPES = {
    'group': u'TraitGroup'
}

ALL_TYPES = {}
ALL_TYPES.update(TRAIT_TYPES)
ALL_TYPES.update(CHOICE_TYPES)
ALL_TYPES.update(GROUP_TYPES)