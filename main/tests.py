from django.test import TestCase, override_settings
from django.urls import reverse


@override_settings(
    CACHES={"default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"}}
)
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
