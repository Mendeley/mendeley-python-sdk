import yaml

from mendeley import Mendeley


def load_config():
    with open('test_config.yml') as f:
        return yaml.load(f)


def configure_mendeley():
    config = load_config()
    return Mendeley(config['clientId'], config['clientSecret'], config['redirectUri'])


def get_access_token():
    config = load_config()
    return config['accessToken']