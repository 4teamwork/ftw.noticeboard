from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import alsoProvides
from zope.interface import implements
from zope.interface import Interface


class INotice(Interface):
    """Marker interface for the Notice"""


class INoticeSchema(model.Schema):
    """A Folderish type for notices, which may hold images"""


class Notice(Container):
    implements(INotice)


alsoProvides(INoticeSchema, IFormFieldProvider)
