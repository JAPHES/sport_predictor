from functools import lru_cache
import warnings

import joblib
from django.conf import settings
from django.shortcuts import render


GENDER_CHOICES = (
    ("1", "Male"),
    ("0", "Female"),
)


SPORT_EXPLANATIONS = {
    "Basketball": {
        "why": (
            "{name}'s age of {age}, height of {height:g} feet, and selected gender ({gender}) "
            "matched a pattern where the model recommends Basketball. This sport often rewards "
            "reach, quick movement, balance, and coordination."
        ),
        "fit": (
            "Basketball may suit {name} because it can help build agility, teamwork, jumping "
            "ability, and confidence while staying active."
        ),
        "motivation": (
            "Keep practicing the basics, stay consistent, and give Basketball a confident try."
        ),
    },
    "Hockey": {
        "why": (
            "{name}'s age of {age}, height of {height:g} feet, and selected gender ({gender}) "
            "matched a pattern where the model recommends Hockey. This sport often favors "
            "focus, speed, coordination, and quick decision-making."
        ),
        "fit": (
            "Hockey may suit {name} because it can improve reaction time, discipline, teamwork, "
            "and body control."
        ),
        "motivation": (
            "Start with the fundamentals, stay patient, and build your skills one session at a time."
        ),
    },
    "Soccer": {
        "why": (
            "{name}'s age of {age}, height of {height:g} feet, and selected gender ({gender}) "
            "matched a pattern where the model recommends Soccer. This sport often values "
            "endurance, footwork, movement, and teamwork."
        ),
        "fit": (
            "Soccer may suit {name} because it can help develop stamina, coordination, game "
            "awareness, and communication with teammates."
        ),
        "motivation": (
            "Keep moving, keep learning, and enjoy every chance to improve on the field."
        ),
    },
}


@lru_cache(maxsize=1)
def load_sport_model():
    model_path = settings.BASE_DIR / "sport_ml_model" / "ml_sports_model.joblib"
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return joblib.load(model_path)


def build_prediction_explanation(predicted_sport, name, age, height, gender):
    gender_label = dict(GENDER_CHOICES).get(str(gender), "Not specified")
    explanation = SPORT_EXPLANATIONS.get(
        predicted_sport,
        {
            "why": (
                "{name}'s submitted details matched a pattern where the model recommends "
                "{sport}."
            ),
            "fit": (
                "{sport} may suit {name} by encouraging movement, discipline, and teamwork."
            ),
            "motivation": "Stay active, keep learning, and enjoy trying the recommended sport.",
        },
    )
    values = {
        "name": name,
        "age": age,
        "height": height,
        "gender": gender_label,
        "sport": predicted_sport,
    }

    return {
        "why": explanation["why"].format(**values),
        "fit": explanation["fit"].format(**values),
        "motivation": explanation["motivation"].format(**values),
    }


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
            context["explanation"] = build_prediction_explanation(
                prediction,
                name,
                age,
                height,
                gender_input,
            )

    return render(request, "predictor.html", context)
