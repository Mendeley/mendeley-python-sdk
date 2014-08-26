import arrow
import pytest
import vcr

from mendeley.exception import MendeleyException
from mendeley.session import MendeleySession
from test import configure_mendeley, get_access_token


@vcr.use_cassette('fixtures/profiles/get_profile/get_profile.yaml', filter_headers=['authorization'])
def test_should_get_a_profile():
    mendeley = configure_mendeley()
    session = MendeleySession(mendeley, get_access_token())

    profile = session.profiles.get('9930207c-c19f-3de0-b531-86bd4388fa94')

    assert profile.id == '9930207c-c19f-3de0-b531-86bd4388fa94'
    assert profile.first_name == 'Jenny'
    assert profile.last_name == 'Johnson'
    assert profile.display_name == 'Jenny Johnson'
    assert not profile.email
    assert profile.link == 'http://www.mendeley.com/profiles/jenny-johnson4/'
    assert not profile.research_interests
    assert profile.academic_status == 'Librarian'
    assert not profile.verified
    assert profile.user_type == 'normal'
    assert profile.created == arrow.get(2014, 8, 26, 15, 24, 45)

    assert profile.discipline.name == 'Humanities'
    assert not profile.discipline.subdisciplines

    assert not profile.photo.original
    assert profile.photo.standard == 'http://s3.amazonaws.com/mendeley-photos/awaiting.png'
    assert profile.photo.square == 'http://s3.amazonaws.com/mendeley-photos/awaiting_square.png'

    assert not profile.location
    assert not profile.education
    assert not profile.employment


@vcr.use_cassette('fixtures/profiles/get_profile/profile_not_found.yaml', filter_headers=['authorization'])
def test_should_raise_if_profile_not_found():
    mendeley = configure_mendeley()
    session = MendeleySession(mendeley, get_access_token())

    with pytest.raises(MendeleyException) as ex_info:
        session.profiles.get('00000000-0000-0001-0000-000000000002')

    ex = ex_info.value
    assert ex.status == 404
    assert ex.message == 'profile not found'