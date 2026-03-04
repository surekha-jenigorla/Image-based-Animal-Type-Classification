import numpy as np
import tensorflow as tf
import os
from django.conf import settings
from PIL import Image
import threading

# ======================================================
# MODEL CONFIG
# ======================================================

MODEL_PATH = os.path.join(
    settings.BASE_DIR,
    "ml_models",
    "cattle_saved_model"   # SavedModel folder
)

CLASS_NAMES = [
    "Gir",
    "Sahiwal",
    "Red Sindhi",
    "Murrah Buffalo",
    "Jersey",
    "Holstein Friesian"
]

_model = None
_infer = None
_model_lock = threading.Lock()


# ======================================================
# SAFE MODEL LOADER (SavedModel)
# ======================================================

def load_model_safe():
    global _model, _infer

    if _model is None:
        with _model_lock:
            if _model is None:
                print("Loading cattle model...")

                _model = tf.saved_model.load(MODEL_PATH)

                # Get inference function
                _infer = _model.signatures["serving_default"]

                print("Model loaded successfully.")

    return _infer


# ======================================================
# IMAGE PREPROCESSING
# ======================================================

def preprocess_image(image: Image.Image):
    image = image.convert("RGB")
    image = image.resize((224, 224))

    arr = np.array(image).astype("float32") / 255.0
    arr = np.expand_dims(arr, axis=0)

    return arr


# ======================================================
# PREDICTION FUNCTION
# ======================================================

def predict_with_local_model(image: Image.Image):
    try:
        infer = load_model_safe()
    except Exception as e:
        print("Model loading failed:", e)
        return {
            "breed": "Unknown",
            "type": "Cattle",
            "confidence": 0
        }

    try:
        img = preprocess_image(image)

        # Run inference
        outputs = infer(tf.constant(img))

        # Extract prediction tensor
        predictions = list(outputs.values())[0].numpy()[0]

        idx = int(np.argmax(predictions))
        confidence = float(predictions[idx] * 100)

        breed = CLASS_NAMES[idx]
        cattle_type = "Buffalo" if "Buffalo" in breed else "Cattle"

        return {
            "breed": breed,
            "type": cattle_type,
            "confidence": round(confidence, 2)
        }

    except Exception as e:
        print("Prediction failed:", e)
        return {
            "breed": "Unknown",
            "type": "Cattle",
            "confidence": 0
        }
