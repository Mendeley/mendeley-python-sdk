from test import cassette, sleep
from test.resources.documents import *


def test_should_iterate_through_search_results():
    session = get_user_session()
    delete_all_documents()

    with cassette('fixtures/resources/documents/iter_search/iterate_through_search_results.yaml'):
        session.documents.create('Underwater basket weaving', 'journal')
        session.documents.create('Underwater bucket weaving', 'journal')
        session.documents.create('Overground basket weaving', 'journal')
        session.documents.create('Underwater basket knitting', 'journal')

        sleep(3)

        docs = list(session.documents.search('basket').iter(page_size=2))
        titles = set([doc.title for doc in docs])
        assert titles == {'Underwater basket weaving', 'Overground basket weaving', 'Underwater basket knitting'}
