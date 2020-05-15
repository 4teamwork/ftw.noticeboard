from plone import api
from zope.publisher.browser import BrowserView


class NoticeBoardView(BrowserView):

    def get_categories(self):
        return self.context.listFolderContents()  # not a catalog query

    def get_categories_and_notices(self):
        """
        Return a prepopulated structure for easy rendering in the template.
        This method could be implented with just one catalog query.
        But as off now there are propbably just a few 100 Notices per installation.
        So caching and improved querying is not necessary right now.
        """
        catalog = api.portal.get_tool('portal_catalog')
        results = []

        for category in self.get_categories():
            notices = catalog(path='/'.join(category.getPhysicalPath()),
                              portal_type='ftw.noticeboard.Notice')
            results.append(
                {
                    'title': category.Title,
                    'url': category.absolute_url(),
                    'notices': [
                        {
                            'title': notice.Title,
                            'url': notice.getURL(),
                            'expires': api.portal.get_localized_time(notice.expires)
                        } for notice in notices
                    ]
                }
            )
        return results
