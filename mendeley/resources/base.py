from future.moves.urllib.parse import urlsplit, parse_qs, urlencode, urlunsplit
from future.utils import iteritems

from mendeley.pagination import Page


class ListResource(object):
    def list(self, page_size=None):
        url = add_query_params(self._url, {'limit': page_size})
        rsp = self._session.get(url, headers={'Accept': self._obj_type.content_type})
        return Page(self._session, rsp, self._obj_type)

    def iter(self, page_size=None):
        page = self.list(page_size)

        while page:
            for item in page.items:
                yield item

            page = page.next_page

    @property
    def _session(self):
        raise NotImplementedError

    @property
    def _url(self):
        raise NotImplementedError

    @property
    def _obj_type(self):
        raise NotImplementedError


def add_query_params(url, params):
    scheme, netloc, path, query_string, fragment = urlsplit(url)
    query_params = parse_qs(query_string)

    for name, value in iteritems(params):
        if value:
            query_params[name] = [value]

    new_query_string = urlencode(query_params, doseq=True)

    return urlunsplit((scheme, netloc, path, new_query_string, fragment))
