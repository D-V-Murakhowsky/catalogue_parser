from unittest import TestCase, skip

from application.page_getter import PageGetter


class TestAllPagesGetting(TestCase):

    @skip
    def test_several_pages_getting(self):
        actual = PageGetter.parse_catalogue_pages()
        pass