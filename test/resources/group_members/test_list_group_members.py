import arrow

from test import get_user_session, cassette


def test_should_list_a_groups_members():
    session = get_user_session()

    with cassette('fixtures/resources/group_members/list_group_members/list_group_members.yaml'):
        page = session.groups.get('bcb12b97-db8a-3c1d-b696-d99ed4371175').members.list()
        assert len(page.items) == 2
        assert page.count == 2

        assert page.items[0].id == '3e71f6e3-e2b4-3f20-a873-da62554c5c38'
        assert page.items[0].role == 'member'
        assert page.items[0].joined == arrow.get(2014, 8, 27, 9, 41, 23)

        assert page.items[1].id == '9930207c-c19f-3de0-b531-86bd4388fa94'
        assert page.items[1].role == 'owner'
        assert page.items[1].joined == arrow.get(2014, 8, 27, 9, 40, 41)


def test_should_list_profiles_for_members():
    session = get_user_session()

    with cassette('fixtures/resources/group_members/list_group_members/list_profiles_for_members.yaml'):
        page = session.groups.get('bcb12b97-db8a-3c1d-b696-d99ed4371175').members.list()
        assert len(page.items) == 2
        assert page.count == 2

        assert page.items[0].display_name == 'Jimmy Jones, PhD'
        assert page.items[0].created == arrow.get(2014, 4, 9, 10, 10, 41)

        assert page.items[1].display_name == 'Jenny Johnson'
        assert page.items[1].created == arrow.get(2014, 8, 26, 15, 24, 45)


def test_should_page_through_group_members():
    session = get_user_session()

    with cassette('fixtures/resources/group_members/list_group_members/page_through_group_members.yaml'):
        first_page = session.groups.get('bcb12b97-db8a-3c1d-b696-d99ed4371175').members.list(page_size=1)
        assert len(first_page.items) == 1
        assert first_page.count == 2

        assert first_page.items[0].id == '3e71f6e3-e2b4-3f20-a873-da62554c5c38'
        assert first_page.items[0].role == 'member'
        assert first_page.items[0].joined == arrow.get(2014, 8, 27, 9, 41, 23)
        assert first_page.items[0].display_name == 'Jimmy Jones, PhD'

        second_page = first_page.next_page
        assert len(second_page.items) == 1
        assert second_page.count == 2

        assert second_page.items[0].id == '9930207c-c19f-3de0-b531-86bd4388fa94'
        assert second_page.items[0].role == 'owner'
        assert second_page.items[0].joined == arrow.get(2014, 8, 27, 9, 40, 41)
        assert second_page.items[0].display_name == 'Jenny Johnson'
