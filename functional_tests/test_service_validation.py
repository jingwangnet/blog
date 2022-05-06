from .base import FunctionalTest
import unittest


class ServicesValidationTest(FunctionalTest):

    @unittest.skip
    def test_cannot_add_empty_services(self):
        self.fail('write me')
