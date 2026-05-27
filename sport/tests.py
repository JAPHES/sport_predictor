from django.test import RequestFactory, SimpleTestCase

from .views import build_prediction_explanation, index, predictor


class PredictorViewTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_landing_page_loads(self):
        request = self.factory.get("/")
        response = index(request)
        content = response.content.decode()

        self.assertEqual(response.status_code, 200)
        self.assertIn("Sports Predictor", content)
        self.assertIn("Start prediction", content)
        self.assertIn("developed by Japhes Murithi", content)

    def test_predictor_page_loads(self):
        request = self.factory.get("/predictor")
        response = predictor(request)
        content = response.content.decode()

        self.assertEqual(response.status_code, 200)
        self.assertIn("Sports Predictor", content)
        self.assertIn("Predict sport", content)
        self.assertIn("developed by Japhes Murithi", content)

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
        self.assertIn("Why this sport was predicted", content)
        self.assertIn("How it may suit the learner", content)
        self.assertIn("Recommendation message", content)
        self.assertIn("reach, quick movement, balance, and coordination", content)

    def test_prediction_explanation_uses_submitted_inputs(self):
        explanation = build_prediction_explanation(
            predicted_sport="Soccer",
            name="Alex",
            age=15,
            height=5.4,
            gender="1",
        )

        self.assertIn("Alex's age of 15", explanation["why"])
        self.assertIn("height of 5.4 feet", explanation["why"])
        self.assertIn("selected gender (Male)", explanation["why"])
        self.assertIn("Soccer may suit Alex", explanation["fit"])
        self.assertTrue(explanation["motivation"])

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

    def test_predictor_rejects_height_outside_allowed_range(self):
        request = self.factory.post(
            "/predictor",
            {
                "name": "Alex",
                "age": "15",
                "height": "9",
                "gender": "1",
            },
        )
        response = predictor(request)
        content = response.content.decode()

        self.assertEqual(response.status_code, 200)
        self.assertIn("Height must be between 2 and 8 feet.", content)
        self.assertNotIn("Recommended game for Alex", content)
