from django.test import TestCase
from django.urls import reverse


class MainAppTests(TestCase):
    def test_static_pages(self):
        pages = [
            "home",
            "calculus",
            "olympiads",
            "pet_peeves",
            "contact",
        ]

        for page in pages:
            with self.subTest(page=page):
                response = self.client.get(reverse(f"main:{page}_page"))
                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, f"main/{page}.html")
