from functools import lru_cache
import warnings

import joblib
from django.conf import settings
from django.shortcuts import render


GENDER_CHOICES = (
    ("1", "Male"),
    ("0", "Female"),
)


@lru_cache(maxsize=1)
def load_sport_model():
    model_path = settings.BASE_DIR / "sport_ml_model" / "ml_sports_model.joblib"
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return joblib.load(model_path)


def index(request):
    return render(request, "index.html")


def predictor(request):
    context = {
        "gender_choices": GENDER_CHOICES,
        "form": {},
        "errors": {},
    }

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        age_input = request.POST.get("age", "").strip()
        height_input = request.POST.get("height", "").strip()
        gender_input = request.POST.get("gender", "").strip()

        context["form"] = {
            "name": name,
            "age": age_input,
            "height": height_input,
            "gender": gender_input,
        }

        errors = {}

        if not name:
            errors["name"] = "Enter a name."

        try:
            age = int(age_input)
            if age < 13 or age > 19:
                errors["age"] = "Age must be between 13 and 19."
        except ValueError:
            errors["age"] = "Enter a valid age."

        try:
            height = float(height_input)
            if height < 2 or height > 8:
                errors["height"] = "Height must be between 2 and 8 feet."
        except ValueError:
            errors["height"] = "Enter a valid height."

        if gender_input not in dict(GENDER_CHOICES):
            errors["gender"] = "Choose a gender."

        context["errors"] = errors

        if not errors:
            model = load_sport_model()
            features = [[age, height, int(gender_input)]]
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                prediction = model.predict(features)[0]

            context["prediction"] = prediction
            context["person_name"] = name

    return render(request, "predictor.html", context)
