def assert_basket_file(file):
    assert file.id
    assert file.size == 178
    assert file.file_name == 'Underwater basket weaving'
    assert file.mime_type == 'text/plain'
    assert file.filehash == '92c7a71b371eb439579be559b5eac9c09a743c42'
    assert file.download_url == 'https://api.mendeley.com/files/%s' % file.id


def assert_weaving_file(file):
    assert file.id
    assert file.size == 196
    assert file.file_name == 'Underwater basket weaving'
    assert file.mime_type == 'text/plain'
    assert file.filehash == '3f7d22ad2bb50ff8a13b9c485f2991e48bc9b5af'
    assert file.download_url == 'https://api.mendeley.com/files/%s' % file.id
