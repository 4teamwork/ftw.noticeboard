from ftw.builder import Builder
from ftw.builder import create
from ftw.noticeboard.tests import FunctionalTestCase
from ftw.testbrowser import browsing
from ftw.testbrowser.pages import factoriesmenu
from ftw.testbrowser.pages import statusmessages
from ftw.testbrowser.pages import plone
from plone.app.textfield.value import RichTextValue


class TestContentTypes(FunctionalTestCase):

    def setUp(self):
        super(TestContentTypes, self).setUp()
        self.grant('Manager')

    @browsing
    def test_add_noticeboard(self, browser):
        browser.login().visit()
        factoriesmenu.add('NoticeBoard')
        browser.fill({'Title': u'This is our NoticeBoard'})
        browser.find_button_by_label('Save').click()
        self.assertEquals(u'This is our NoticeBoard', plone.first_heading())

    @browsing
    def test_add_noticecategory(self, browser):
        noticeboard = create(Builder('noticeboard').titled(u'Noticeboard'))

        browser.login().visit(noticeboard)
        factoriesmenu.add('NoticeCategory')
        browser.fill({'Title': u'This is a Category', 'Terms and Conditions': 'Anything'})
        browser.find_button_by_label('Save').click()
        self.assertEquals(u'This is a Category', plone.first_heading())

    @browsing
    def test_add_notice(self, browser):
        noticeboard = create(Builder('noticeboard').titled(u'Noticeboard'))
        category = create(Builder('noticecategory')
                          .having(conditions=RichTextValue('Something'))
                          .titled(u'Category')
                          .within(noticeboard))

        browser.login().visit(category)
        factoriesmenu.add('Notice')
        browser.fill({'Title': u'This is a Notice', 'Terms and Conditions': True})
        browser.find_button_by_label('Save').click()
        self.assertEquals(u'This is a Notice', plone.first_heading())

    @browsing
    def test_terms_and_conditions_need_to_be_accepted(self, browser):
        noticeboard = create(Builder('noticeboard').titled(u'Noticeboard'))
        category = create(Builder('noticecategory')
                          .having(conditions=RichTextValue('Something'))
                          .titled(u'Category')
                          .within(noticeboard))

        browser.login().visit(category)
        factoriesmenu.add('Notice')
        browser.fill({'Title': u'This is a Notice'})
        browser.find_button_by_label('Save').click()
        self.assertEquals(u'Add Notice', plone.first_heading())
        statusmessages.assert_message('There were some errors.')
