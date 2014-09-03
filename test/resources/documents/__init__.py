import arrow
from test import load_config, get_user_session


def delete_all_documents():
    config = load_config()
    session = get_user_session()

    if config['recordMode'] != 'none':
        for doc in session.documents.iter():
            doc.delete()


def create_document(session, title='Underwater basket weaving'):
    return session.documents.create(title,
                                    'journal',
                                    source='Journal of Submarine Bambrology',
                                    year=2014,
                                    abstract='The wonders of creating exotic baskets in an underwater environment',
                                    identifiers={'doi': 'doi123'},
                                    keywords=['bambrology', 'submarine'],
                                    pages='1-6',
                                    volume='loud',
                                    issue='73',
                                    websites=['http://example.com/foo', 'http://example.com/bar'],
                                    month=11,
                                    publisher='Elsevier',
                                    day=14,
                                    city='Scunthorpe',
                                    edition='First',
                                    institution='University of Cambridge',
                                    series='World Series',
                                    chapter='99',
                                    revision='2',
                                    accessed=arrow.get(2014, 9, 3),
                                    read=False,
                                    starred=True,
                                    authored=False,
                                    confirmed=True,
                                    tags=['baskety', 'wet'])


def assert_core_document(doc):
    assert doc.id
    assert doc.title == 'Underwater basket weaving'
    assert doc.type == 'journal'
    assert doc.source == 'Journal of Submarine Bambrology'
    assert doc.year == 2014
    assert doc.abstract == 'The wonders of creating exotic baskets in an underwater environment'
    assert doc.identifiers['doi'] == 'doi123'
    assert doc.keywords == ['bambrology', 'submarine']
    assert doc.created
    assert doc.last_modified


def assert_bib_document(doc):
    assert doc.pages == '1-6'
    assert doc.volume == 'loud'
    assert doc.issue == '73'
    assert doc.websites == ['http://example.com/foo', 'http://example.com/bar']
    assert doc.month == 11
    assert doc.publisher == 'Elsevier'
    assert doc.day == 14
    assert doc.city == 'Scunthorpe'
    assert doc.edition == 'First'
    assert doc.institution == 'University of Cambridge'
    assert doc.series == 'World Series'
    assert doc.chapter == '99'
    assert doc.revision == '2'
    assert doc.accessed == arrow.get(2014, 9, 3)


def assert_client_document(doc):
    assert not doc.read
    assert doc.starred
    assert not doc.authored
    assert doc.confirmed
    assert not doc.hidden


def assert_tags_document(doc):
    assert doc.tags == ['baskety', 'wet']
