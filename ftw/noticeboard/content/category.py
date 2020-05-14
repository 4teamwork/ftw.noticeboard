from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implements
from zope.interface import Interface


class INoticeCategory(Interface):
    """Marker interface for the Notice category"""


class INoticeCategorySchema(model.Schema):
    """A Folderish type for notices categories, which holds notices"""


class NoticeCategory(Container):
    implements(INoticeCategory)
