import vcr

import yaml

from mendeley import Mendeley
from mendeley.session import MendeleySession


def load_config_from_file(filename):
    with open(filename) as f:
        return yaml.load(f)


def load_config():
    try:
        return load_config_from_file('test_config.yml')
    except IOError:
        return load_config_from_file('test_config.yml.default')


def configure_mendeley():
    config = load_config()
    return Mendeley(config['clientId'], config['clientSecret'], config['redirectUri'])


def get_user_session():
    config = load_config()
    mendeley = configure_mendeley()

    return MendeleySession(mendeley, config['accessToken'])


def get_client_credentials_session():
    config = load_config()
    mendeley = configure_mendeley()

    if config['recordMode'] == 'none':
        return MendeleySession(mendeley, config['accessToken'])
    else:
        return mendeley.start_client_credentials_flow().authenticate()


def cassette(path):
    config = load_config()
    return vcr.use_cassette(path, filter_headers=['authorization'], record_mode=config['recordMode'])
