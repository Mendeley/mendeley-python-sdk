import arrow
import pytest
from mendeley.exception import MendeleyApiException

from test import get_user_session, cassette


def test_should_get_a_group():
    session = get_user_session()

    with cassette('fixtures/resources/groups/get_group/get_group.yaml'):
        group = session.groups.get('bcb12b97-db8a-3c1d-b696-d99ed4371175')

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

        assert group.owner.id == '9930207c-c19f-3de0-b531-86bd4388fa94'
        assert group.owner.display_name == 'Jenny Johnson'


def test_should_be_able_to_get_owner_id_without_getting_profile():
    session = get_user_session()

    with cassette('fixtures/resources/groups/get_group/get_owner_id_without_getting_profile.yaml') as cass:
        group = session.groups.get('bcb12b97-db8a-3c1d-b696-d99ed4371175')
        owner = group.owner

        assert owner.id == '9930207c-c19f-3de0-b531-86bd4388fa94'

    assert len(cass.requests) == 1


def test_should_only_get_owner_profile_once():
    session = get_user_session()

    with cassette('fixtures/resources/groups/get_group/only_get_profile_once.yaml') as cass:
        group = session.groups.get('bcb12b97-db8a-3c1d-b696-d99ed4371175')
        owner = group.owner

        assert owner.first_name == 'Jenny'
        assert owner.last_name == 'Johnson'

    assert len(cass.requests) == 2


def test_should_raise_if_group_not_found():
    session = get_user_session()

    with cassette('fixtures/resources/groups/get_group/group_not_found.yaml'), \
            pytest.raises(MendeleyApiException) as ex_info:
        session.groups.get('00000000-0000-0001-0000-000000000002')

    ex = ex_info.value
    assert ex.status == 404
    assert ex.message == 'Group [00000000-0000-0001-0000-000000000002] does not exist'
