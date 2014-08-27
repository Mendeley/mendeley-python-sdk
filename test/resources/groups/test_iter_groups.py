import pytest

from test import get_user_session, cassette


def test_should_iterate_through_groups():
    session = get_user_session()

    with cassette('fixtures/resources/groups/iter_groups/iterate_through_groups.yaml'):
        groups = session.groups.iter(page_size=1)

        first_group = next(groups)
        assert first_group.id == '164d48fb-2343-332d-b566-1a4884a992e4'
        assert first_group.name == 'Basket weaving'

        assert first_group.owner.id == '3e71f6e3-e2b4-3f20-a873-da62554c5c38'
        assert first_group.owner.display_name == 'Jimmy Jones, PhD'

        second_group = next(groups)

        assert second_group.id == 'bcb12b97-db8a-3c1d-b696-d99ed4371175'
        assert second_group.name == 'Python SDK Test Group'

        assert second_group.owner.id == '9930207c-c19f-3de0-b531-86bd4388fa94'
        assert second_group.owner.display_name == 'Jenny Johnson'

        with pytest.raises(StopIteration):
            _ = next(groups)