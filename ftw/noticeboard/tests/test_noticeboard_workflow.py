from ftw.builder import Builder
from ftw.builder import create
from ftw.noticeboard.tests import FunctionalTestCase
from ftw.testbrowser import browsing
from ftw.testbrowser.pages import factoriesmenu
from ftw.testbrowser.pages import plone
from plone.app.textfield.value import RichTextValue


class TestNoticeBoardWorkflow(FunctionalTestCase):

    def setUp(self):
        super(TestNoticeBoardWorkflow, self).setUp()
        self.grant('Manager')

    @browsing
    def test_user_can_only_add_and_edit_notices(self, browser):
        user = create(Builder('user'))
        browser.login(user).visit()
        with self.assertRaises(ValueError):
            # ValueError: Cannot add "NoticeBoard": no factories menu visible
            factoriesmenu.add('NoticeBoard')

        noticeboard = create(Builder('noticeboard'))
        browser.visit(noticeboard)

        with self.assertRaises(ValueError):
            # ValueError: Cannot add "NoticeBoard": no factories menu visible
            factoriesmenu.add('NoticeCategory')

        category = create(Builder('noticecategory').within(noticeboard))
        browser.visit(category)
        factoriesmenu.add('Notice')

        browser.fill(
            {
                'Title': u'This is a Notice',
                'Price': '100',
                'Terms and Conditions': True,
                'E-Mail': u'hans@peter.example',
                'Text': u'Anything',
            }
        )
        browser.find_button_by_label('Save').click()
        self.assertEquals(u'This is a Notice', plone.first_heading())

        browser.visit('@@edit')
        browser.fill(
            {
                'Title': u'Changed',
            }
        )
        browser.find_button_by_label('Save').click()
        self.assertEquals(u'Changed', plone.first_heading())

    @browsing
    def test_user_can_only_add_images_on_notices_he_created(self, browser):
        user = create(Builder('user'))

        noticeboard = create(Builder('noticeboard'))
        category = create(Builder('noticecategory').within(noticeboard))
        othernotice = create(Builder('notice')
                             .titled(u'This is a Notice')
                             .having(accept_conditions=True,
                                     text=RichTextValue('Something'),
                                     price='100')
                             .within(category))

        browser.login(user).visit(othernotice)
        self.assertFalse(factoriesmenu.visible())

        browser.visit(category)
        factoriesmenu.add('Notice')

        browser.fill(
            {
                'Title': u'This is a Notice',
                'Price': '100',
                'Terms and Conditions': True,
                'E-Mail': u'hans@peter.example',
                'Text': u'Anything',
            }
        )
        browser.find_button_by_label('Save').click()
        self.assertEqual(
            ['NoticeImage', ],
            factoriesmenu.addable_types())
