from future.moves.urllib.parse import urlsplit, parse_qs, urlencode, urlunsplit

from mendeley.pagination import Page


class ListResource(object):
    def __init__(self, session, base_url, content_type, obj_type):
        self.session = session
        self.base_url = base_url
        self.content_type = content_type
        self.obj_type = obj_type

    def list(self, page_size=None):
        rsp = self.session.get(add_query_param(self.base_url, 'limit', page_size),
                               headers={'Accept': self.content_type})
        return Page(self.session, rsp, self.obj_type)

    def iter(self, page_size=None):
        page = self.list(page_size)

        while page:
            for item in page.items:
                yield item

            page = page.next_page


def add_query_param(url, name, value):
    if not value:
        return url

    scheme, netloc, path, query_string, fragment = urlsplit(url)
    query_params = parse_qs(query_string)

    query_params[name] = [value]
    new_query_string = urlencode(query_params, doseq=True)

    return urlunsplit((scheme, netloc, path, new_query_string, fragment))
