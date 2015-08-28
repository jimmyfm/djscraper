from http.client import HTTPConnection

from bs4 import BeautifulSoup

from django.core.management.base import BaseCommand

from project import settings
from scraper.models import Categoria


# TODO Logging ammodo
class Command(BaseCommand):
    help = 'Sincronizza categorie con DB'

    @staticmethod
    def retrieve_cats():
        print('Pre Retrieve Page')
        conn = HTTPConnection(settings.SCRAP_HOST)
        headers = settings.SCRAP_HEADERS.copy()
        headers.update({'Cookie': settings.SCRAP_COOKIE})
        conn.request("GET", "/area_soci_mip.asp", None, headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()

        print('Page retrieved, analyzing')

        res = []
        soup = BeautifulSoup(data, 'html.parser')
        rows = soup.find('select', {'name': 'codmar'}).find_all('option')
        print('Processing %s entry' % len(rows))

        if len(rows) == 0:
            raise ValueError('no valid records on page')

        for r in rows:
            codice = r['value'].strip()
            if codice.isdigit():
                nome = r.text.strip()
                o = type('Dummy', (object,), {'codice': codice, 'nome': nome})
                res.append(o)
        else:
            print('a')

        return res

    def handle(self, *args, **options):
        cats = self.retrieve_cats()

        print('Processing %s cats' % len(cats))
        for c in cats:
            q = Categoria.objects.filter(codice=c.codice)
            print(q)
            if not q.count():
                print('New Cat')
                cat = Categoria(codice=c.codice, nome=c.nome)
                cat.save()
            else:
                print('Existing Cat')

                cat = q.first()
                if c.nome != cat.nome:
                    print('Update Info')
                    cat.nome = c.nome
                    cat.save()

                pass
                # TODO Verifica categorie non aggiornate
