import arrow

from test import get_user_session, cassette


def test_should_get_groups():
    session = get_user_session()

    with cassette('fixtures/resources/groups/list_groups/list_groups.yaml'):
        page = session.groups.list()
        assert len(page.items) == 2
        assert page.count == 2

        assert page.items[0].id == '164d48fb-2343-332d-b566-1a4884a992e4'
        assert page.items[0].name == 'Basket weaving'
        assert page.items[0].description == 'All of the best papers about weaving baskets'
        assert page.items[0].disciplines == ['Arts and Literature']
        assert page.items[0].tags == ['baskets', 'weaving']
        assert page.items[0].webpage == 'http://example.com/baskets'
        assert page.items[0].created == arrow.get(2014, 5, 20, 11, 40, 22)
        assert page.items[0].link == 'http://www.mendeley.com/groups/4499471/basket-weaving/'
        assert page.items[0].access_level == 'public'
        assert page.items[0].role == 'member'

        assert page.items[0].photo.original == \
            'http://s3.amazonaws.com/mendeley-photos/73/e3/73e38a6a2cad3d760c04c1f7ef8a35ecf3f2d110.png'
        assert page.items[0].photo.standard == \
            'http://s3.amazonaws.com/mendeley-photos/73/e3/73e38a6a2cad3d760c04c1f7ef8a35ecf3f2d110-standard.jpg'
        assert page.items[0].photo.square == \
            'http://s3.amazonaws.com/mendeley-photos/73/e3/73e38a6a2cad3d760c04c1f7ef8a35ecf3f2d110-square.jpg'

        assert page.items[0].owner.id == '3e71f6e3-e2b4-3f20-a873-da62554c5c38'
        assert page.items[0].owner.display_name == 'Jimmy Jones, PhD'

        assert page.items[1].id == 'bcb12b97-db8a-3c1d-b696-d99ed4371175'
        assert page.items[1].name == 'Python SDK Test Group'
        assert page.items[1].description == 'Test group for the Mendeley Python SDK'
        assert page.items[1].disciplines == ['Computer and Information Science', 'Humanities']
        assert page.items[1].tags == ['python', 'sdk']
        assert page.items[1].webpage == 'http://dev.mendeley.com'
        assert page.items[1].created == arrow.get(2014, 8, 27, 9, 40, 41)
        assert page.items[1].link == 'http://www.mendeley.com/groups/4779311/python-sdk-test-group/'
        assert page.items[1].access_level == 'public'
        assert page.items[1].role == 'owner'

        assert page.items[1].photo.original == \
            'http://s3.amazonaws.com/mendeley-photos/a0/20/a020f9fd30af0029c059c45535ad231d3d0d055a.png'
        assert page.items[1].photo.standard == \
            'http://s3.amazonaws.com/mendeley-photos/a0/20/a020f9fd30af0029c059c45535ad231d3d0d055a-standard.jpg'
        assert page.items[1].photo.square == \
            'http://s3.amazonaws.com/mendeley-photos/a0/20/a020f9fd30af0029c059c45535ad231d3d0d055a-square.jpg'

        assert page.items[1].owner.id == '9930207c-c19f-3de0-b531-86bd4388fa94'
        assert page.items[1].owner.display_name == 'Jenny Johnson'


def test_should_page_through_groups():
    session = get_user_session()

    with cassette('fixtures/resources/groups/list_groups/page_through_groups.yaml'):
        first_page = session.groups.list(page_size=1)
        assert len(first_page.items) == 1
        assert first_page.count == 2

        assert first_page.items[0].id == '164d48fb-2343-332d-b566-1a4884a992e4'
        assert first_page.items[0].name == 'Basket weaving'

        assert first_page.items[0].owner.id == '3e71f6e3-e2b4-3f20-a873-da62554c5c38'
        assert first_page.items[0].owner.display_name == 'Jimmy Jones, PhD'

        second_page = first_page.next_page
        assert len(second_page.items) == 1
        assert second_page.count == 2

        assert second_page.items[0].id == 'bcb12b97-db8a-3c1d-b696-d99ed4371175'
        assert second_page.items[0].name == 'Python SDK Test Group'

        assert second_page.items[0].owner.id == '9930207c-c19f-3de0-b531-86bd4388fa94'
        assert second_page.items[0].owner.display_name == 'Jenny Johnson'
