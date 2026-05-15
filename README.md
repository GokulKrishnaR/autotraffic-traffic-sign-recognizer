# Auto Traffic — Traffic Sign Recognizer

**Repository:** https://github.com/GokulKrishnaR/autotraffic-traffic-sign-recognizer

Single-page app: **upload an image** or **live camera detection** for 43 traffic sign classes (TensorFlow `Traffic.h5`).

## Run locally

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open http://127.0.0.1:8000/

## Deploy on Render

1. Push this repo to GitHub.
2. [render.com](https://render.com) → **New → Blueprint** (uses `render.yaml`) or **Web Service**.
3. Connect repo `GokulKrishnaR/autotraffic-traffic-sign-recognizer`.
4. Environment variables:
   - `DEBUG` = `False`
   - `SECRET_KEY` = (random string)
   - `ALLOWED_HOSTS` = `your-service-name.onrender.com`
5. Deploy. First build may take 10–20 minutes (TensorFlow).

**Live camera** on the hosted site: open the URL (HTTPS), scroll to **Live detection**, click **Start camera**, allow permission.

## Project layout

| Path | Purpose |
|------|---------|
| `textapp/views.py` | Home page + prediction API |
| `textapp/sign_predictor.py` | Model inference |
| `template/home.html` | Upload + live camera UI |
| `Traffic.h5` | Trained model (required) |
