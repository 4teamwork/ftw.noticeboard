from ftw.builder import Builder
from ftw.builder import create
from ftw.noticeboard.tests import FunctionalTestCase
from ftw.testbrowser import browsing
from ftw.testbrowser.pages import factoriesmenu
from ftw.testbrowser.pages import plone


class TestContentTypes(FunctionalTestCase):

    @browsing
    def test_add_noticeboard(self, browser):
        self.grant('Manager')
        browser.login().visit()
        factoriesmenu.add('NoticeBoard')
        browser.fill({'Title': u'This is our NoticeBoard'})
        browser.find_button_by_label('Save').click()
        self.assertEquals(u'This is our NoticeBoard', plone.first_heading())

    @browsing
    def test_add_noticecategory(self, browser):
        self.grant('Manager')

        noticeboard = create(Builder('noticeboard').titled(u'Noticeboard'))

        browser.login().visit(noticeboard)
        factoriesmenu.add('NoticeCategory')
        browser.fill({'Title': u'This is a Category'})
        browser.find_button_by_label('Save').click()
        self.assertEquals(u'This is a Category', plone.first_heading())

    @browsing
    def test_add_notice(self, browser):
        self.grant('Manager')

        noticeboard = create(Builder('noticeboard').titled(u'Noticeboard'))
        category = create(Builder('noticecategory').titled(u'Category').within(noticeboard))

        browser.login().visit(category)
        factoriesmenu.add('Notice')
        browser.fill({'Title': u'This is a Notice'})
        browser.find_button_by_label('Save').click()
        self.assertEquals(u'This is a Notice', plone.first_heading())
