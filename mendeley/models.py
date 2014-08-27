import arrow

from mendeley.response import ResponseObject


class Discipline(ResponseObject):
    @classmethod
    def fields(cls):
        return ['name', 'subdisciplines']


class Photo(ResponseObject):
    @classmethod
    def fields(cls):
        return ['original', 'standard', 'square']


class Location(ResponseObject):
    @classmethod
    def fields(cls):
        return ['latitude', 'longitude', 'name']


class Education(ResponseObject):
    @property
    def start_date(self):
        if 'start_date' in self.json:
            return arrow.get(self.json['start_date'])
        else:
            return

    @property
    def end_date(self):
        if 'end_date' in self.json:
            return arrow.get(self.json['end_date'])
        else:
            return None

    @classmethod
    def fields(cls):
        return ['institution', 'degree', 'website']


class Employment(ResponseObject):
    @property
    def start_date(self):
        if 'start_date' in self.json:
            return arrow.get(self.json['start_date'])
        else:
            return

    @property
    def end_date(self):
        if 'end_date' in self.json:
            return arrow.get(self.json['end_date'])
        else:
            return None

    @classmethod
    def fields(cls):
        return ['institution', 'position', 'website', 'classes']
