import arrow

from test import get_user_session, cassette


def test_should_get_groups():
    session = get_user_session()

    with cassette('fixtures/resources/groups/get_groups/get_groups.yaml'):
        groups = session.groups.list()
        assert len(groups) == 1

        group = groups[0]
        owner = group.owner

        assert group.id == 'bcb12b97-db8a-3c1d-b696-d99ed4371175'
        assert group.name == 'Python SDK Test Group'
        assert group.description == 'Test group for the Mendeley Python SDK'
        assert group.disciplines == ['Computer and Information Science', 'Humanities']
        assert group.tags == ['python', 'sdk']
        assert group.webpage == 'http://dev.mendeley.com'
        assert group.created == arrow.get(2014, 8, 27, 9, 40, 41)
        assert group.link == 'http://www.mendeley.com/groups/4779311/python-sdk-test-group/'
        assert group.access_level == 'public'
        assert group.role == 'owner'

        assert group.photo.original == \
            'http://s3.amazonaws.com/mendeley-photos/a0/20/a020f9fd30af0029c059c45535ad231d3d0d055a.png'
        assert group.photo.standard == \
            'http://s3.amazonaws.com/mendeley-photos/a0/20/a020f9fd30af0029c059c45535ad231d3d0d055a-standard.jpg'
        assert group.photo.square == \
            'http://s3.amazonaws.com/mendeley-photos/a0/20/a020f9fd30af0029c059c45535ad231d3d0d055a-square.jpg'

        assert owner.id == '9930207c-c19f-3de0-b531-86bd4388fa94'
        assert owner.display_name == 'Jenny Johnson'
