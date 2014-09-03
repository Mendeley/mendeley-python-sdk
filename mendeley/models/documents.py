import arrow
from mendeley.models.base_documents import BaseDocument, BaseClientView, BaseBibView
from mendeley.models.profiles import LazyProfile


class UserDocument(BaseDocument):
    @property
    def created(self):
        if 'created' in self._json:
            return arrow.get(self._json['created'])
        else:
            return None

    @property
    def last_modified(self):
        if 'last_modified' in self._json:
            return arrow.get(self._json['last_modified'])
        elif 'created' in self._json:
            return arrow.get(self._json['created'])
        else:
            return None

    @property
    def profile(self):
        if 'profile_id' in self._json:
            return LazyProfile(self.session, self._json['profile_id'])
        else:
            return None

    def delete(self):
        self.session.documents.delete(self.id)


class UserBibView(BaseBibView):
    @property
    def accessed(self):
        if 'accessed' in self._json:
            return arrow.get(self._json['accessed'])
        else:
            return None


class UserClientView(BaseClientView):
    @classmethod
    def fields(cls):
        return super(UserClientView, cls).fields() + ['read', 'starred', 'authored', 'confirmed', 'hidden']


class UserTagsView(object):
    @classmethod
    def fields(cls):
        return ['tags']


class UserBibDocument(UserDocument, UserBibView):
    @classmethod
    def fields(cls):
        return UserDocument.fields() + UserBibView.fields()


class UserClientDocument(UserDocument, UserClientView):
    @classmethod
    def fields(cls):
        return UserDocument.fields() + UserClientView.fields()


class UserTagsDocument(UserDocument, UserTagsView):
    @classmethod
    def fields(cls):
        return UserDocument.fields() + UserTagsView.fields()


class UserAllDocument(UserDocument, UserBibView, UserClientView, UserTagsView):
    @classmethod
    def fields(cls):
        return UserDocument.fields() + UserBibView.fields() + UserClientView.fields() + UserTagsView.fields()
