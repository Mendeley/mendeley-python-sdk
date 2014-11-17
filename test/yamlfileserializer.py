from vcr.serializers import yamlserializer


class YamlFileSerializer(object):
    def serialize(self, cassette_dict):
        cassette_dict['interactions'] = [self.__read_file(i) for i in cassette_dict['interactions']]
        if 'body' in cassette_dict and hasattr(cassette_dict['body'], 'read'):
            cassette_dict['body'] = cassette_dict['body'].read()

        return yamlserializer.serialize(cassette_dict)


    def deserialize(self, cassette_string):
        return yamlserializer.deserialize(cassette_string)


    @staticmethod
    def __read_file(interaction):
        if 'request' in interaction \
                and 'body' in interaction['request'] \
                and hasattr(interaction['request']['body'], 'read'):
            with open(interaction['request']['body'].name, 'rb') as f:
                interaction['request']['body'] = f.read()

        return interaction