from django.test import TestCase
from django.urls import reverse


class BasicTests(TestCase):
    def test_home(self):
        r = self.client.get(reverse("pages:home"))
        self.assertEqual(r.status_code, 200)

    def test_about(self):
        r = self.client.get(reverse("pages:about"))
        self.assertEqual(r.status_code, 200)

    def test_language_switch(self):
        r = self.client.post(reverse("set_language"), {"language": "en", "next": "/"})
        self.assertIn(r.status_code, (302, 200))

    def test_privacy(self):
        r = self.client.get(reverse("pages:privacy"))
        self.assertEqual(r.status_code, 200)

    def test_terms(self):
        r = self.client.get(reverse("pages:terms"))
        self.assertEqual(r.status_code, 200)