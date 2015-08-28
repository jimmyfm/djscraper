from django.core import management
from django.test import TestCase


class TestSyncCat(TestCase):
    def test_sync_cat(self):
        management.call_command('sync_cat')
