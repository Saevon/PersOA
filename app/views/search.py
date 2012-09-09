from app.models.choice import BasicChoice, LinearChoice, SubChoice
from app.models.group import TraitGroup
from app.models.trait import BasicTrait, LinearTrait

from utils.decorators import cascade
from whoosh import index
import os

class WhooshIndex(object):

    INDICES = {}

    def __init__(self, indexdir):
        self._indexdir = indexdir
        self._writer = None

    @staticmethod
    def get(indexdir=None, flush=False):
        if not WhooshIndex.INDICES.has_key(indexdir):
            WhooshIndex.INDICES[indexdir] = (WhooshIndex(indexdir)
                .open_index(flush=flush)
            )

        return WhooshIndex.INDICES[indexdir]

    def create_schema(self, flush=False):
        from whoosh.fields import Schema
        from whoosh.fields import ID, KEYWORD, TEXT
        from shutil import rmtree

        schema = Schema(
            # Identification
            name=TEXT(stored=True),
            kind=ID(stored=True),
            # Searching
            keywords=KEYWORD,
            defn=TEXT,
            desc=TEXT,
        )

        # Remove the old index if flushing
        if flush:
            rmtree(self._indexdir)

        # Create the folder if needed
        if not os.path.exists(self._indexdir):
            os.mkdir(self._indexdir)

        # make the actual index
        self.index = index.create_in(self._indexdir, schema)
        self.refresh_index()

    @cascade
    def open_index(self, flush=False):
        if not os.path.exists(self._indexdir) or flush:
            self.create_schema(flush=flush)
        else:
            self.index = index.open_dir(self._indexdir)

    def refresh_index(self):
        from itertools import chain

        items = chain(
            BasicChoice.objects.all(), LinearChoice.objects.all(), SubChoice.objects.all(),
            TraitGroup.objects.all(),
            BasicTrait.objects.all(), LinearTrait.objects.all(),
        )

        for item in items:
            data = self.index_data(item)
            self.writer.update_document(**data)
        self.writer.commit()

    @property
    def writer(self):
        if self._writer is None:
            self._writer = self.index.writer()
        return self._writer

    def search(self, *args):
        pass

    def index_data(self, item):
        data = {}

        # Choices
        if isinstance(item, BasicChoice):
            data = {
                'name': item.name,
                'kind': u'BasicChoice',
                'keywords': u'%s choice' % (item.name),
                'desc': item.desc,
                'defn': item.defn,
            }
        elif isinstance(item, LinearChoice):
            data = {
                'name': item.name,
                'kind': u'LinearChoice',
                'keywords': u'%s choice' % (item.name),
                'desc': item.desc,
                'defn': item.defn,
            }
        elif isinstance(item, SubChoice):
            data = {
                'name': item.name,
                'kind': u'SubChoice',
                'keywords': u'%s %s subchoice choice' %
                    (item.choice.name, item.name),
                'desc': item.desc,
                'defn': item.desc,
            }
        # Groups
        elif isinstance(item, TraitGroup):
            data = {
                'name': item.name,
                'kind': u'TraitGroup',
                'keywords': u'%s group' % (item.name),
                'desc': item.desc,
                'defn': item.desc,
            }
        # Traits
        elif isinstance(item, BasicTrait):
            data = {
                'name': item.name,
                'kind': u'BasicTrait',
                'keywords': u'%s trait' % (item.name),
                'desc': item.desc,
                'defn': item.defn,
            }
        elif isinstance(item, LinearTrait):
                data = {
                'name': item.name,
                'kind': u'LinearTrait',
                'keywords': u'%s trait' % (item.name),
                'desc': item.desc,
                'defn': item.defn,
            }

        return data

