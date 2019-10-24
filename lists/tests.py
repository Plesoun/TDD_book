from django.test import TestCase


class TestTest(TestCase):

	def test_bad(self):
		self.assertEqual(1 + 1, 3)
