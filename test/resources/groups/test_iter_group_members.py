import arrow
import pytest

from test import get_user_session, cassette


def test_should_iterate_through_group_members():
    session = get_user_session()

    with cassette('fixtures/resources/groups/iter_group_members/iterate_through_group_members.yaml'):
        members = session.groups.get('bcb12b97-db8a-3c1d-b696-d99ed4371175').members.iter(page_size=1)

        first_member = next(members)
        assert first_member.id == '3e71f6e3-e2b4-3f20-a873-da62554c5c38'
        assert first_member.role == 'member'
        assert first_member.joined == arrow.get(2014, 8, 27, 9, 41, 23)
        assert first_member.display_name == 'Jimmy Jones, PhD'

        second_member = next(members)
        assert second_member.id == '9930207c-c19f-3de0-b531-86bd4388fa94'
        assert second_member.role == 'owner'
        assert second_member.joined == arrow.get(2014, 8, 27, 9, 40, 41)
        assert second_member.display_name == 'Jenny Johnson'

        with pytest.raises(StopIteration):
            _ = next(members)
