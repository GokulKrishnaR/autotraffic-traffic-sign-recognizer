# Auto Traffic — Traffic Sign Recognizer

Django web application that classifies traffic signs from uploaded images using a TensorFlow/Keras CNN (`Traffic.h5`). It also supports live webcam detection with text-to-speech on a local machine.

## Project structure

| Path | Purpose |
|------|---------|
| `textproject/` | Django project settings and URLs |
| `textapp/` | Views, models, templates, static files |
| `template/` | HTML templates (login, upload, prediction) |
| `predict.py` | Image classification logic |
| `Traffic.h5` | Trained CNN model (required at project root) |
| `manage.py` | Django management commands |
| `clientApp.py` | Standalone Flask API (optional, port 5000) |
| `Model Training/` | Notebook, training scripts, dataset (not required to run the app) |

## Features

- User registration and login (SQLite)
- Admin panel to view/delete users
- **Upload image** → predict one of 43 German traffic sign classes
- **Live webcam** (`/udp/`) → real-time detection with TTS (local only; needs a camera)

## Run locally

### Prerequisites

- Python 3.10 or 3.11 (recommended)
- `Traffic.h5` in the project root

### Setup

```bash
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements-deploy.txt
python manage.py migrate
python manage.py runserver
```

Open http://127.0.0.1:8000/

> **Note:** `req.txt` is a full machine export and is not used for deployment. Use `requirements-deploy.txt` instead.

## Deploy to the web

GitHub **does not host** Django apps directly (GitHub Pages only serves static sites). Use this flow:

1. **Push code to GitHub** (this repository).
2. **Deploy on [Render](https://render.com)** (free tier) — connects to your GitHub repo and runs the app.

### Render (recommended)

1. Push this repo to GitHub.
2. Sign in at [render.com](https://render.com) with GitHub.
3. **New → Blueprint** and select this repo (uses `render.yaml`), **or** **New → Web Service** with:
   - **Build command:** `pip install -r requirements-deploy.txt && python manage.py collectstatic --noinput && python manage.py migrate --noinput`
   - **Start command:** `gunicorn textproject.wsgi:application`
   - **Environment:** `DEBUG=False`, `ALLOWED_HOSTS=your-app.onrender.com`
4. Ensure `Traffic.h5` is committed (≈13 MB).

Live webcam (`/udp/`) will not work on cloud servers (no camera). Image upload works.

### Other options

- **Railway / Fly.io / Azure / AWS:** same start command as Render; set env vars from `textproject/settings.py`.
- **Docker:** `Dockerfile` runs the Flask `clientApp.py`; for Django, change the CMD to `gunicorn textproject.wsgi:application`.

## Environment variables

| Variable | Description |
|----------|-------------|
| `SECRET_KEY` | Django secret (required in production) |
| `DEBUG` | `True` locally, `False` on Render |
| `ALLOWED_HOSTS` | Comma-separated hostnames, e.g. `myapp.onrender.com` |

## Large files not in Git

These are excluded via `.gitignore` (over GitHub’s 100 MB limit or size):

- `*.weights` (YOLO weights ~235 MB each)
- `Model Training/Train/` and `Model Training/Test/` datasets

Keep them on your machine or add them as [GitHub Releases](https://docs.github.com/en/repositories/releasing-projects-on-github) if you need to share them.
