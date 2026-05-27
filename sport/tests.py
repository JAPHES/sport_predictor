from django.test import RequestFactory, SimpleTestCase

from .views import predictor


class PredictorViewTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_predictor_page_loads(self):
        request = self.factory.get("/predictor")
        response = predictor(request)
        content = response.content.decode()

        self.assertEqual(response.status_code, 200)
        self.assertIn("Sports Predictor", content)
        self.assertIn("Predict sport", content)

    def test_predictor_returns_sport_for_valid_form(self):
        request = self.factory.post(
            "/predictor",
            {
                "name": "Alex",
                "age": "13",
                "height": "5",
                "gender": "1",
            },
        )
        response = predictor(request)
        content = response.content.decode()

        self.assertEqual(response.status_code, 200)
        self.assertIn("Recommended game for Alex", content)
        self.assertIn("Basketball", content)

    def test_predictor_rejects_age_outside_allowed_range(self):
        request = self.factory.post(
            "/predictor",
            {
                "name": "Alex",
                "age": "20",
                "height": "5",
                "gender": "1",
            },
        )
        response = predictor(request)
        content = response.content.decode()

        self.assertEqual(response.status_code, 200)
        self.assertIn("Age must be between 13 and 19.", content)
        self.assertNotIn("Recommended game for Alex", content)
