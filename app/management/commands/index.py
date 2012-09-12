from django.core.management.base import BaseCommand

from app.constants.index import INDEX_DIR
from app.views.search import WhooshIndex
from optparse import make_option
from textwrap import dedent

class Command(BaseCommand):
    help = 'Creates with the search index'

    option_list = BaseCommand.option_list + (
        make_option('--flush',
            action='store_true',
            dest='flush',
            default=False,
            help='Remake the index from scratch'
        ),
    )

    def handle(self, *args, **options):
        index = WhooshIndex.get(INDEX_DIR)
        index.create_schema(flush=options['flush'])

