from pkg_resources import get_distribution
from plone import api
from Products.Five.browser import BrowserView


IS_PLONE_5 = get_distribution('Plone').version >= '5'


class NoticeView(BrowserView):

    def get_localized_expiration_date(self):
        return api.portal.get_localized_time(self.context.expires())

    def can_edit(self):
        return api.user.has_permission('Modify portal content', obj=self.context)

    def show_plone5_upload(self):
        return IS_PLONE_5
