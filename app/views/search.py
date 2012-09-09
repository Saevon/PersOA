from app.models.choice import BasicChoice, LinearChoice, SubChoice
from app.models.group import TraitGroup
from app.models.trait import BasicTrait, LinearTrait

from collections import defaultdict
from utils.decorators import cascade
from whoosh import index
from whoosh.qparser import MultifieldParser, OrGroup, QueryParser
from whoosh.query import Term
import os

class WhooshIndex(object):

    INDICES = {}

    CLASSES = {'choice': [], 'group': [], 'trait': [], 'all': [], 'index': {}}
    for cls in [BasicTrait, LinearTrait]:
        CLASSES['index'][cls.__name__] = cls
        CLASSES['all'].append(unicode(cls.__name__))
        CLASSES['trait'].append(unicode(cls.__name__))

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
            id=ID(stored=True),
            type=ID(stored=True),
            # Searching
            name=TEXT,
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
            self.writer.add_document(**data)
        self.writer.commit()

    @property
    def writer(self):
        if self._writer is None:
            self._writer = self.index.writer()
        return self._writer

    def search(self, **kwargs):
        kwargs = defaultdict(unicode, **kwargs)
        with self.index.searcher() as searcher:
            query = (QueryParser('keywords', self.index.schema)
                .parse(unicode(kwargs.get('query', u'').lower()))
            )

            if len(kwargs['name']):
                query = (query & QueryParser(u'name', self.index.schema)
                    .parse(" ".join([
                        unicode(i) for i in kwargs['name']
                    ]))
                )
            if len(kwargs['desc']):
                query = (query
                    & MultifieldParser([u'desc', u'defn'], self.index.schema)
                        .parse(" ".join([
                            unicode(i) for i in kwargs['desc']
                        ]))
                )

            if kwargs['type']:
                query = (
                    QueryParser(u'type', self.index.schema, group=OrGroup).parse(" ".join(kwargs['type']))
                    & query
                )

            print query
            results = [hit.fields() for hit in
                searcher.search(query, limit=1)
            ]
            return results

    def index_data(self, item):
        data = {}

        # Choices
        if isinstance(item, BasicChoice):
            data = {
                'name': item.name,
                'type': u'BasicChoice',
                'keywords': u'%s choice' % (item.name),
                'desc': item.desc,
                'defn': item.defn,
            }
        elif isinstance(item, LinearChoice):
            data = {
                'name': item.name,
                'type': u'LinearChoice',
                'keywords': u'%s choice' % (item.name),
                'desc': item.desc,
                'defn': item.defn,
            }
        elif isinstance(item, SubChoice):
            data = {
                'name': item.name,
                'type': u'SubChoice',
                'keywords': u'%s %s subchoice choice' %
                    (item.choice.name, item.name),
                'desc': u'',
                'defn': item.defn,
            }
        # Groups
        elif isinstance(item, TraitGroup):
            data = {
                'name': item.name,
                'type': u'TraitGroup',
                'keywords': u'%s group' % (item.name),
                'desc': item.desc,
                'defn': u'',
            }
        # Traits
        elif isinstance(item, BasicTrait):
            data = {
                'name': item.name,
                'type': u'BasicTrait',
                'keywords': u'%s trait' % (item.name),
                'desc': item.desc,
                'defn': item.defn,
            }
        elif isinstance(item, LinearTrait):
            data = {
                'name': item.name,
                'type': u'LinearTrait',
                'keywords': u'%s %s %s trait' % (
                    item.name, item.pos_name, item.neg_name
                ),
                'desc': item.desc,
                'defn': item.defn,
            }
        data['id'] = unicode(item.id)
        data['keywords'] = data['keywords'].lower()

        return data

