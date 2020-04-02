from ftw.noticeboard.interfaces import INotice
from plone.app.dexterity.behaviors.metadata import IBasic
from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import alsoProvides
from zope.interface import implementer
from zope.interface import implements
from zope.schema.interfaces import ICollection


@implementer(ICollection)
class INoticeSchema(model.Schema):
    """
    This schema represents a notice item.
    """
    pass


alsoProvides(INoticeSchema, IBasic)


class Notice(Container):
    implements(INotice)

