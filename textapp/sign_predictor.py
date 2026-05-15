import base64
import os

import cv2
import numpy as np
import tensorflow as tf
from django.conf import settings

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

CONFIDENCE_THRESHOLD = float(os.environ.get("PREDICTION_CONFIDENCE", "0.85"))

_model = None


def get_model_path():
    path = settings.BASE_DIR / "Traffic.h5"
    if not path.exists():
        raise FileNotFoundError(f"Model not found at {path}")
    return str(path)


def get_model():
    global _model
    if _model is None:
        _model = tf.keras.models.load_model(get_model_path())
    return _model


def predict_from_rgb_array(rgb_image):
    resized = cv2.resize(rgb_image, (30, 30))
    input_data = np.expand_dims(resized, axis=0) / 255.0
    pred = get_model().predict(input_data, verbose=0)
    confidence = float(pred.max())
    class_index = int(pred.argmax())
    label = SIGN_LABELS[class_index] if class_index < len(SIGN_LABELS) else "Unknown"
    if confidence < CONFIDENCE_THRESHOLD:
        return {
            "prediction": None,
            "confidence": confidence,
            "class_index": class_index,
            "below_threshold": True,
        }
    return {
        "prediction": label,
        "confidence": confidence,
        "class_index": class_index,
        "below_threshold": False,
    }


def predict_from_base64(image_b64):
    if "," in image_b64:
        image_b64 = image_b64.split(",", 1)[1]
    raw = base64.b64decode(image_b64)
    arr = np.frombuffer(raw, dtype=np.uint8)
    image = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if image is None:
        return {"error": "Invalid image data"}
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return predict_from_rgb_array(rgb)
