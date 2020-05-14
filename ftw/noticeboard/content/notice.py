from ftw.noticeboard import _
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.content import Container
from plone.supermodel import model
from z3c.form import validator
from zope import schema
from zope.interface import alsoProvides
from zope.interface import implements
from zope.interface import Interface
from zope.interface import Invalid


class INotice(Interface):
    """Marker interface for the Notice"""


class INoticeSchema(model.Schema):
    """A Folderish type for notices, which may hold images"""

    accept_conditions = schema.Bool(
        title=_(u'label_accept_conditions', default=u'Terms and Conditions'),
        description=_(u'description_accept_conditions',
                      default=u'Please accept the '
                      '<a target="_blank" href="./terms_and_conditions">terms and conditions</a>'),
        default=False)


class Notice(Container):
    implements(INotice)


alsoProvides(INoticeSchema, IFormFieldProvider)


class AcceptedTermsAndConditions(validator.SimpleFieldValidator):
    """ z3c.form validator class for international phone numbers """

    def validate(self, value):
        if not value:
            raise Invalid(_(u'You need to accept the terms and conditions'))
        return


validator.WidgetValidatorDiscriminators(
    AcceptedTermsAndConditions,
    field=INoticeSchema['accept_conditions']
)
