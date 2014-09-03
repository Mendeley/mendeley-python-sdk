from future.moves.urllib.parse import urlsplit, parse_qs, urlencode, urlunsplit
from future.utils import iteritems

from mendeley.pagination import Page


class ListResource(object):
    def list(self, page_size=None, **kwargs):
        return self._list(page_size, **kwargs)

    def iter(self, page_size=None, **kwargs):
        page = self._list(page_size, **kwargs)

        while page:
            for item in page.items:
                yield item

            page = page.next_page

    def _list(self, page_size, **kwargs):
        obj_type = self._obj_type(**kwargs)
        kwargs['limit'] = page_size
        url = add_query_params(self._url, kwargs)
        rsp = self._session.get(url, headers={'Accept': obj_type.content_type})
        return Page(self._session, rsp, obj_type)

    @property
    def _session(self):
        raise NotImplementedError

    @property
    def _url(self):
        raise NotImplementedError

    def _obj_type(self, **kwargs):
        raise NotImplementedError


def add_query_params(url, params):
    scheme, netloc, path, query_string, fragment = urlsplit(url)
    query_params = parse_qs(query_string)

    for name, value in iteritems(params):
        if value:
            query_params[name] = [value]

    new_query_string = urlencode(query_params, doseq=True)

    return urlunsplit((scheme, netloc, path, new_query_string, fragment))
