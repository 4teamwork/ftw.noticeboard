from ftw.builder import Builder
from ftw.builder import create
from ftw.noticeboard.tests import FunctionalTestCase
from ftw.testbrowser import browsing
from ftw.testbrowser.pages import factoriesmenu
from parameterized import parameterized
import json


class TestCategoryPermission(FunctionalTestCase):

    @parameterized.expand([('Site Administrator', 'can add'), ('Contributor', 'can not add')])
    @browsing
    def test_category_type_add_permission(self, role, expectation, browser):
        """
        Make sure that the Permission for adding Categories works correctly.
        """
        self.grant('Site Administrator')
        page = create(Builder('folder'))
        user = create(Builder('user').with_roles(role, on=page))
        browser.login(user).visit(page)
        # Try to add a new Category
        try:
            # When the expectation 'can add' is, then this should work fine.
            # When the expectation 'can not add' is, then this should fail.
            factoriesmenu.add('Category')
            if expectation == 'can not add':
                self.fail('The role {} shouldn\'t be able to add a new Category type.'.format(role))
        except ValueError as e:
            if 'The type "Category" is not addable' in e.message and expectation == 'can add':
                self.fail('The role {} should be able to add a new Category type.'.format(role))

        # When the expectation 'can not add' is, then this point should never be reached in the code
        # because it should fail above.
