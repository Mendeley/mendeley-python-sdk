import arrow

from test import get_user_session, cassette


def test_should_get_a_groups_members():
    session = get_user_session()

    with cassette('fixtures/resources/groups/get_group_members/get_group_members.yaml'):
        members = session.groups.get('bcb12b97-db8a-3c1d-b696-d99ed4371175').members.list()
        assert len(members) == 2

        assert members[0].id == '3e71f6e3-e2b4-3f20-a873-da62554c5c38'
        assert members[0].role == 'member'
        assert members[0].joined == arrow.get(2014, 8, 27, 9, 41, 23)

        assert members[1].id == '9930207c-c19f-3de0-b531-86bd4388fa94'
        assert members[1].role == 'owner'
        assert members[1].joined == arrow.get(2014, 8, 27, 9, 40, 41)


def test_should_get_profiles_for_members():
    session = get_user_session()

    with cassette('fixtures/resources/groups/get_group_members/get_profiles_for_members.yaml'):
        members = session.groups.get('bcb12b97-db8a-3c1d-b696-d99ed4371175').members.list()
        assert len(members) == 2

        assert members[0].display_name == 'Jimmy Jones, PhD'
        assert members[0].created == arrow.get(2014, 4, 9, 10, 10, 41)

        assert members[1].display_name == 'Jenny Johnson'
        assert members[1].created == arrow.get(2014, 8, 26, 15, 24, 45)