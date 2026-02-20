from django.test import TestCase
from django.urls import reverse


class IndexViewTests(TestCase):
    def test_index_contains_prediction(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('prediction', response.context)
        self.assertContains(response, response.context['prediction'])
