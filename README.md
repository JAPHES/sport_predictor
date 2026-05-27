# Sports Predictor

Sports Predictor is a Django machine learning web app that recommends a suitable sport for a learner based on age, height, and gender. The prediction model is a saved scikit-learn decision tree model.

The project was developed by **Japhes Murithi**.

## Live Demo

```text
https://sportpredictor-production.up.railway.app
```

## Features

- Landing page with navbar, hero section, project highlights, and footer.
- Predictor form for name, age, height, and gender.
- Age validation restricted to learners between 13 and 19 years.
- Machine learning prediction using a saved `.joblib` model.
- Supports predictions for Basketball, Hockey, and Soccer.
- Railway-ready deployment configuration.

## Tech Stack

- Python 3.12
- Django 4.2.11
- scikit-learn
- joblib
- WhiteNoise
- Gunicorn
- Railway

## Project Structure

```text
sportpredictor/
|-- manage.py
|-- requirements.txt
|-- railway.toml
|-- .python-version
|-- sport/
|   |-- templates/
|   |   |-- index.html
|   |   `-- predictor.html
|   |-- static/
|   |   `-- sport/images/sports-ml-hero.png
|   |-- tests.py
|   |-- urls.py
|   `-- views.py
|-- sport_ml_model/
|   `-- ml_sports_model.joblib
`-- sportpredictor/
    |-- settings.py
    |-- urls.py
    `-- wsgi.py
```

## Model Inputs

The saved model expects three features:

```text
Age
Height
Sex
```

The user also enters a name, but the name is only used to personalize the result. It is not used by the machine learning model.

Gender is encoded as:

```text
Male = 1
Female = 0
```

## Local Setup

From the `sportpredictor` folder:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open the app:

```text
http://127.0.0.1:8000/
```

Open the predictor directly:

```text
http://127.0.0.1:8000/predictor
```

## Running Tests

```powershell
python manage.py check
python manage.py test sport
```

## Railway Deployment

This project includes:

- `requirements.txt`
- `.python-version`
- `railway.toml`
- WhiteNoise static file configuration
- Gunicorn start command

If your GitHub repository root is the `sportpredictor` folder, Railway can deploy from it directly.

If your GitHub repository root is the outer `SPORTS` folder, set the Railway root directory to:

```text
/sportpredictor
```

Add these Railway environment variables:

```text
DJANGO_DEBUG=False
DJANGO_SECRET_KEY=your-long-random-secret-key
```

Generate a Django secret key locally with:

```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

After pushing to GitHub, Railway should automatically detect the latest commit and redeploy the app.

## Important Files

- `sport/views.py` loads the model and handles prediction.
- `sport/templates/index.html` contains the landing page.
- `sport/templates/predictor.html` contains the prediction form.
- `sport_ml_model/ml_sports_model.joblib` is required for predictions.

## Notes

The model was originally trained with scikit-learn `1.6.1`, so the project pins `scikit-learn==1.6.1` in `requirements.txt` for deployment reliability.
