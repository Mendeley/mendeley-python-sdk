class MendeleyException(Exception):
    pass


class MendeleyApiException(MendeleyException):
    def __init__(self, rsp):
        self.rsp = rsp

    @property
    def status(self):
        return self.rsp.status_code

    @property
    def message(self):
        try:
            return self.rsp.json()['message']
        except ValueError:
            return self.rsp.text
