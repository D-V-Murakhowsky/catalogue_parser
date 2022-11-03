from unittest import TestCase, skip

from application.selenium_connector.page_getter import PageGetter


class TestSeveralPagesGetting(TestCase):

    @skip
    def test_several_pages_getting(self):
        actual = PageGetter.parse_catalogue_pages()
        pass