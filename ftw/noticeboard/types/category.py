from ftw.noticeboard.interfaces import ICategory
from plone.app.dexterity.behaviors.metadata import IBasic
from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import alsoProvides
from zope.interface import implementer
from zope.interface import implements
from zope.schema.interfaces import ICollection


@implementer(ICollection)
class ICategorySchema(model.Schema):
    """
    This schema represents a category item.
    """
    pass


alsoProvides(ICategorySchema, IBasic)


class Category(Container):
    implements(ICategory)
