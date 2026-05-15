# Auto Traffic — Traffic Sign Recognizer

**Final Year Undergraduate Project** — B.Sc. Computer Applications (CA)

**Live demo:** [https://autotraffic-traffic-sign-recognizer.onrender.com/](https://autotraffic-traffic-sign-recognizer.onrender.com/)

**Repository:** [https://github.com/GokulKrishnaR/autotraffic-traffic-sign-recognizer](https://github.com/GokulKrishnaR/autotraffic-traffic-sign-recognizer)

A web application that recognizes traffic signs using a convolutional neural network (TensorFlow/Keras). Upload an image or use your device camera for real-time detection across **43 German traffic sign classes**.

## Features

- **Image upload** — submit a photo and get the predicted sign class
- **Live detection** — browser camera sends frames to the server for continuous recognition (works on the hosted site over HTTPS)

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
   - `ALLOWED_HOSTS` = `autotraffic-traffic-sign-recognizer.onrender.com`
5. Deploy. First build may take 10–20 minutes (TensorFlow).

## Project layout

| Path | Purpose |
|------|---------|
| `textapp/views.py` | Home page + prediction API |
| `textapp/sign_predictor.py` | Model inference |
| `template/home.html` | Upload + live camera UI |
| `Traffic.h5` | Trained model (required) |
