import arrow

from test import get_user_session, cassette


def test_should_get_groups():
    session = get_user_session()

    with cassette('fixtures/resources/groups/get_groups/get_groups.yaml'):
        groups = session.groups.list()
        assert len(groups) == 1

        assert groups[0].id == 'bcb12b97-db8a-3c1d-b696-d99ed4371175'
        assert groups[0].name == 'Python SDK Test Group'
        assert groups[0].description == 'Test group for the Mendeley Python SDK'
        assert groups[0].disciplines == ['Computer and Information Science', 'Humanities']
        assert groups[0].tags == ['python', 'sdk']
        assert groups[0].webpage == 'http://dev.mendeley.com'
        assert groups[0].created == arrow.get(2014, 8, 27, 9, 40, 41)
        assert groups[0].link == 'http://www.mendeley.com/groups/4779311/python-sdk-test-group/'
        assert groups[0].access_level == 'public'
        assert groups[0].role == 'owner'

        assert groups[0].photo.original == \
            'http://s3.amazonaws.com/mendeley-photos/a0/20/a020f9fd30af0029c059c45535ad231d3d0d055a.png'
        assert groups[0].photo.standard == \
            'http://s3.amazonaws.com/mendeley-photos/a0/20/a020f9fd30af0029c059c45535ad231d3d0d055a-standard.jpg'
        assert groups[0].photo.square == \
            'http://s3.amazonaws.com/mendeley-photos/a0/20/a020f9fd30af0029c059c45535ad231d3d0d055a-square.jpg'

        assert groups[0].owner.id == '9930207c-c19f-3de0-b531-86bd4388fa94'
        assert groups[0].owner.display_name == 'Jenny Johnson'
