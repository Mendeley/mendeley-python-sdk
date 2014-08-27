from memoized_property import memoized_property


class Page(object):
    def __init__(self, session, rsp, obj_type, count=None):
        self.session = session
        self.rsp = rsp
        self.obj_type = obj_type

        if count:
            self.count = count
        elif 'mendeley-count' in self.rsp.headers:
            self.count = int(self.rsp.headers.get('mendeley-count'))
        else:
            self.count = len(self.items)

    @memoized_property
    def items(self):
        return [self.obj_type(self.session, i) for i in self.rsp.json()]

    def _navigate(self, rel):
        if rel not in self.rsp.links:
            return None
        rsp = self.session.get(self.rsp.links[rel]['url'])
        return Page(self.session, rsp, self.obj_type, self.count)

    @property
    def first_page(self):
        return self._navigate('first')

    @property
    def last_page(self):
        return self._navigate('next')

    @property
    def next_page(self):
        return self._navigate('next')

    @property
    def previous_page(self):
        return self._navigate('prev')