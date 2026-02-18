from django.test import SimpleTestCase
from app import calc


class CalculatorTests(SimpleTestCase):

    def test_sum(self):
        response = calc.sum(6, 7)
        self.assertEqual(response, 13)

    def test_sub(self):
        res = calc.sub(5, 2)
        self.assertEqual(res, 3)
