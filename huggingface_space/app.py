"""
Hugging Face Space — Auto Traffic Sign Recognizer
Uses Pillow for resize only (no OpenCV) so `pip install` is smaller and more reliable on HF.
"""
import os

import gradio as gr
import numpy as np
import tensorflow as tf
from PIL import Image

SIGN_LABELS = [
    "Speed limit (20km/h)", "Speed limit (30km/h)", "Speed limit (50km/h)", "Speed limit (60km/h)",
    "Speed limit (70km/h)", "Speed limit (80km/h)", "End of speed limit (80km/h)", "Speed limit (100km/h)",
    "Speed limit (120km/h)", "No passing", "No passing vehicle over 3.5 tons", "Right-of-way at intersection",
    "Priority road", "Yield", "Stop", "No vehicles", "Vehicle over 3.5 tons prohibited", "No entry",
    "General caution", "Dangerous curve left", "Dangerous curve right", "Double curve", "Bumpy road",
    "Slippery road", "Road narrows on the right", "Road work", "Traffic signals", "Pedestrians",
    "Children crossing", "Bicycles crossing", "Beware of ice/snow", "Wild animals crossing",
    "End speed and passing limits", "Turn right ahead", "Turn left ahead", "Ahead only",
    "Go straight or right", "Go straight or left", "Keep right", "Keep left",
    "Roundabout mandatory", "End of no passing", "End of no passing vehicle over 3.5 tons",
]

CONFIDENCE_THRESHOLD = 0.85
MODEL_PATH = os.path.join(os.path.dirname(__file__), "Traffic.h5")

_model = None


def get_model():
    global _model
    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                "Traffic.h5 not found. Upload it to this Space (same folder as app.py)."
            )
        _model = tf.keras.models.load_model(MODEL_PATH, compile=False)
    return _model


def predict_sign(image):
    if image is None:
        return "Please upload an image or use your webcam."

    # Gradio gives RGB numpy array (H, W, 3)
    arr = image.astype("uint8")
    if len(arr.shape) == 2:
        arr = np.stack([arr, arr, arr], axis=-1)
    elif arr.shape[-1] == 4:
        arr = arr[:, :, :3]

    pil = Image.fromarray(arr, mode="RGB")
    pil = pil.resize((30, 30), Image.Resampling.LANCZOS)
    resized = np.asarray(pil, dtype=np.float32) / 255.0
    input_data = np.expand_dims(resized, axis=0)
    pred = get_model().predict(input_data, verbose=0)
    confidence = float(pred.max())
    class_index = int(pred.argmax())
    label = SIGN_LABELS[class_index] if class_index < len(SIGN_LABELS) else "Unknown"

    if confidence < CONFIDENCE_THRESHOLD:
        return (
            f"No sign detected (low confidence)\n"
            f"Best guess: {label}\n"
            f"Confidence: {confidence * 100:.1f}%"
        )

    return f"**{label}**\n\nConfidence: {confidence * 100:.1f}%"


DESCRIPTION = """
# Auto Traffic — Traffic Sign Recognizer

**Final Year UG Project** | B.Sc. Computer Applications (Triple Main)  
Sacred Heart College, Thevara

Traffic sign recognition using **TensorFlow** and a **CNN** (43 German traffic sign classes).

- **Upload** a photo of a sign, or  
- **Webcam** — allow camera access, then capture/use live feed  

Also deployed on Render: [autotraffic-traffic-sign-recognizer.onrender.com](https://autotraffic-traffic-sign-recognizer.onrender.com/)
"""

demo = gr.Interface(
    fn=predict_sign,
    inputs=gr.Image(
        label="Traffic sign image",
        sources=["upload", "webcam"],
        type="numpy",
    ),
    outputs=gr.Textbox(label="Prediction", lines=4),
    title="Auto Traffic Sign Recognizer",
    description=DESCRIPTION,
    examples=None,
    allow_flagging="never",
)

if __name__ == "__main__":
    demo.launch()
