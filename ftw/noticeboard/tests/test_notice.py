from ftw.builder import Builder
from ftw.builder import create
from ftw.noticeboard.tests import FunctionalTestCase
from ftw.testbrowser import browsing
from ftw.testbrowser.pages import factoriesmenu
from parameterized import parameterized
import json


class TestNoticePermission(FunctionalTestCase):

    @browsing
    def test_can_create_notice_in_category(self, browser):
        """
        Make sure that it's possible to add new Categories and Notices.
        """
        self.grant('Site Administrator')
        page = create(Builder('folder'))
        user = create(Builder('user').with_roles('Site Administrator', on=page))
        browser.login(user).visit(page)
        # Add a new Category
        factoriesmenu.add('Category')
        browser.fill({'Title': 'MyCategory',
                      'Summary Used in item listings and search results.': 'It\'s a Category.'}).submit()
        # Add a new Notice
        factoriesmenu.add('Notice')
        browser.fill({'Title': 'MyNotice',
                      'Summary Used in item listings and search results.': 'It\'s a Notice.'}).submit()

        assert 'MyNotice' in browser.css('#parent-fieldname-title').first.text_content()

    @parameterized.expand([('Site Administrator', 'can not add'), ('Contributor', 'can add')])
    @browsing
    def test_notice_type_add_permission(self, role, expectation, browser):
        """
        Make sure that the Permission for adding Categories works correctly.
        """
        self.grant('Site Administrator')
        page = create(Builder('ftw.noticeboard.Category'))
        user = create(Builder('user').with_roles(role, on=page))
        browser.login(user).visit(page)
        # Try to add a new Notice
        try:
            # When the expectation 'can add' is, then this should work fine.
            # When the expectation 'can not add' is, then this should fail.
            factoriesmenu.add('Notice')
            if expectation == 'can not add':
                self.fail('The role {} shouldn\'t be able to add a new Category type.'.format(role))
        except ValueError as e:
            if 'The type "Category" is not addable' in e.message and expectation == 'can add':
                self.fail('The role {} should be able to add a new Category type.'.format(role))

        # When the expectation 'can not add' is, then this point should never be reached in the code
        # because it should fail above.
