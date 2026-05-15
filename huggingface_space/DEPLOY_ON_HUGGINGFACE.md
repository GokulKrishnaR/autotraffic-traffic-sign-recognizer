# Deploy on Hugging Face (beginner guide)

Follow these steps to publish your app as a **Gradio Space** (free public link).

---

## Before you start

You need:

1. A [Hugging Face](https://huggingface.co/) account (sign up with email or GitHub).
2. The model file **`Traffic.h5`** from the main project folder (about 13 MB).
3. The files in this folder: `app.py`, `requirements.txt`, `README.md`, and `Traffic.h5`.

---

## Step 1 — Create a Space

1. Go to [https://huggingface.co/new-space](https://huggingface.co/new-space).
2. **Space name:** e.g. `auto-traffic-sign-recognizer` (lowercase, no spaces).
3. **License:** MIT (or any you prefer).
4. **Select the Space SDK:** choose **Gradio**.
5. **Space hardware:** **CPU basic** (free) is enough.
6. **Visibility:** Public (so you get a shareable link).
7. Click **Create Space**.

You will get an empty Space and a Git URL like:  
`https://huggingface.co/spaces/YourUsername/auto-traffic-sign-recognizer`

---

## Step 2 — Upload your files

### Option A — Upload in the browser (easiest)

1. On your Space page, open the **Files** tab.
2. Click **Add file** → **Upload files**.
3. Upload these **four** files from the `huggingface_space` folder:
   - `app.py`
   - `requirements.txt`
   - `README.md`
   - `Traffic.h5` (copy from the main project root — **required**)
4. Commit message: `Add Gradio app and model`
5. Click **Commit**.

Hugging Face will **automatically build** the Space (5–15 minutes the first time).

### Option B — Upload with Git (optional)

1. Install [Git](https://git-scm.com/).
2. Clone your Space (replace `YourUsername` and space name):

   ```bash
   git clone https://huggingface.co/spaces/YourUsername/auto-traffic-sign-recognizer
   cd auto-traffic-sign-recognizer
   ```

3. Copy into this folder:
   - `app.py`, `requirements.txt`, `README.md` from `huggingface_space/`
   - `Traffic.h5` from the main project root
4. Run:

   ```bash
   git add app.py requirements.txt README.md Traffic.h5
   git commit -m "Initial Gradio app"
   git push
   ```

   Use your HF username and a [write token](https://huggingface.co/settings/tokens) when Git asks for a password.

---

## Step 3 — Wait for the build

1. Open the **Logs** or **App** tab on your Space.
2. Status will show **Building** then **Running**.
3. If it fails, open the log and check for missing `Traffic.h5` or TensorFlow errors.

---

## Step 4 — Test your app

1. When status is **Running**, open your Space URL:  
   `https://huggingface.co/spaces/YourUsername/auto-traffic-sign-recognizer`
2. **Upload** a traffic sign image, or click the **webcam** icon and allow camera access.
3. You should see the predicted sign name and confidence.

---

## Step 5 — Share the link

Use this URL in your report, resume, or GitHub README:

`https://huggingface.co/spaces/YourUsername/auto-traffic-sign-recognizer`

You can keep your Render link as well — both can point to the same project.

---

## Common problems

| Problem | Fix |
|--------|-----|
| Runtime: `cannot import name 'HfFolder' from 'huggingface_hub'` | Gradio **4.44** is incompatible with newer `huggingface_hub` on Spaces. Use **`sdk_version: 5.12.0`** (or newer Gradio 5) in `README.md` YAML and **`flagging_mode="never"`** instead of `allow_flagging` in `app.py` — use the latest files from this repo's `huggingface_space/` folder. |
| Build fails: `Traffic.h5` not found | Upload `Traffic.h5` to the **root** of the Space (same level as `app.py`). |
| Build very slow or times out | Normal first time (TensorFlow is large). Click **Factory rebuild** and wait again. |
| Webcam does not work | Use **Chrome/Edge**, allow camera permission; HF Spaces support webcam on HTTPS. |
| "Low confidence" always | Hold the sign closer; good lighting; use a clear photo of one sign. |
| Space is sleeping | Free CPU Spaces may pause when idle; open the link and wait ~1 minute. |

---

## What you do NOT need on Hugging Face

- Django, `manage.py`, or `render.yaml` — only the files in `huggingface_space/` plus `Traffic.h5`.
- Login or database — Gradio Space is a single public demo page.

---

## Need help?

- Hugging Face docs: [Spaces — Gradio](https://huggingface.co/docs/hub/spaces-sdks-gradio)
- Your main GitHub repo: [autotraffic-traffic-sign-recognizer](https://github.com/GokulKrishnaR/autotraffic-traffic-sign-recognizer)
