import arrow
import pytest

from mendeley.exception import MendeleyException
from test import get_user_session, cassette, get_client_credentials_session


def test_should_get_my_profile():
    session = get_user_session()

    with cassette('fixtures/resources/profiles/get_my_profile/get_my_profile.yaml'):
        profile = session.profiles.me

        assert profile.id == '3e71f6e3-e2b4-3f20-a873-da62554c5c38'
        assert profile.first_name == 'Jimmy'
        assert profile.last_name == 'Jones'
        assert profile.display_name == 'Jimmy Jones, PhD'
        assert profile.email == 'matt.thomson+jimothy@mendeley.com'
        assert profile.link == 'http://www.mendeley.com/profiles/jimmy-jones5/'
        assert profile.research_interests == 'Underwater basket weaving'
        assert profile.academic_status == 'Post Doc'
        assert profile.verified
        assert profile.user_type == 'normal'
        assert profile.created == arrow.get(2014, 4, 9, 10, 10, 41)

        assert profile.discipline.name == 'Arts and Literature'
        assert profile.discipline.subdisciplines == ['Culture Heritage']

        assert profile.photo.original == \
            'http://s3.amazonaws.com/mendeley-photos/ea/4c/ea4c185e63d3ced8a3c555b397c65869b716f13a.png'
        assert profile.photo.standard == \
            'http://s3.amazonaws.com/mendeley-photos/ea/4c/ea4c185e63d3ced8a3c555b397c65869b716f13a-standard.jpg'
        assert profile.photo.square == \
            'http://s3.amazonaws.com/mendeley-photos/ea/4c/ea4c185e63d3ced8a3c555b397c65869b716f13a-square.jpg'

        assert profile.location.latitude == 3.16
        assert profile.location.longitude == 101.71
        assert profile.location.name == 'Kuala Lumpur, Malaysia'

        assert len(profile.education) == 2
        assert profile.education[0].institution == 'Universiti Kuala Lumpur'
        assert profile.education[0].degree == 'PhD'
        assert profile.education[0].start_date == arrow.get(2009, 9, 1)
        assert profile.education[0].end_date == arrow.get(2012, 8, 1)
        assert profile.education[0].website == 'http://www.unikl.edu.my/'

        assert len(profile.employment) == 2
        assert profile.employment[1].institution == 'Universiti Kuala Lumpur'
        assert profile.employment[1].position == 'Professor of Submarine Bambrology'
        assert profile.employment[1].start_date == arrow.get(2012, 9, 1)
        assert profile.employment[1].end_date == arrow.get(2013, 12, 1)
        assert profile.employment[1].website == 'http://www.unikl.edu.my/'
        assert profile.employment[1].classes == ['Underwater Basket Weaving I', 'Underwater Basket Weaving II']


def test_raise_exception_if_client_credentials():
    session = get_client_credentials_session()

    with cassette('fixtures/resources/profiles/get_my_profile/client_credentials.yaml'), \
            pytest.raises(MendeleyException) as ex_info:
        _ = session.profiles.me

    ex = ex_info.value
    assert ex.status == 400
    assert ex.message == 'No userid found in auth token'
