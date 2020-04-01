from ftw.builder.content import at_content_builders_registered
from ftw.builder.content import register_at_content_builders
from ftw.builder.testing import BUILDER_LAYER
from ftw.builder.testing import functional_session_factory
from ftw.builder.testing import set_builder_session_factory
from plone.app.testing import FunctionalTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.testing import z2
from zope.configuration import xmlconfig


class NoticeboardLayer(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE, BUILDER_LAYER)

    def setUpZope(self, app, configurationContext):
        xmlconfig.string(
            '<configure xmlns="http://namespaces.zope.org/zope">'
            '  <include package="z3c.autoinclude" file="meta.zcml" />'
            '  <includePlugins package="plone" />'
            '  <includePluginsOverrides package="plone" />'
            '</configure>',
            context=configurationContext)

        z2.installProduct(app, 'ftw.noticeboard')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'ftw.noticeboard:default')


NOTICEBOARD_FIXTURE = NoticeboardLayer()
NOTICEBOARD_FUNCTIONAL = FunctionalTesting(
    bases=(NOTICEBOARD_FIXTURE,
           set_builder_session_factory(functional_session_factory)),
    name="ftw.noticeboard:functional")
