from django.test import TestCase

from server.calculator.config_calculator import ExpressionCalculation


class TestExpressionCalculation(TestCase):

    def setUp(self):
        self.calc = ExpressionCalculation()

    def test_evaluate(self):
        self.assertEqual(self.calc.evaluate("3+5"), 8)
