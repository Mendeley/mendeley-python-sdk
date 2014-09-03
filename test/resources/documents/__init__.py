from test import load_config, get_user_session


def delete_all_documents():
    config = load_config()
    session = get_user_session()

    if config['recordMode'] != 'none':
        for doc in session.documents.iter():
            doc.delete()


def create_document(session):
    return session.documents.create('Underwater basket weaving', 'journal')


def assert_core_document(doc):
    assert doc.id
    assert doc.title == 'Underwater basket weaving'
    assert doc.type == 'journal'