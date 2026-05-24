import os
import numpy as np
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from PIL import Image
import io

# ──────────────────────────────────────────────
# Try to load TensorFlow/Keras model
# If not available, fall back to demo mode
# ──────────────────────────────────────────────
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model', 'pneumonia_model.h5')
model = None

try:
    from tensorflow.keras.models import load_model
    if os.path.exists(MODEL_PATH):
        model = load_model(MODEL_PATH)
        print("✅ Real CNN model loaded successfully.")
    else:
        print("⚠️  No model file found at model/pneumonia_model.h5 — running in DEMO mode.")
except ImportError:
    print("⚠️  TensorFlow not installed — running in DEMO mode.")

# ──────────────────────────────────────────────
# Flask app setup
# ──────────────────────────────────────────────
app = Flask(__name__)
app.secret_key = "pneumonia_secret_key_2024"

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
MAX_CONTENT_LENGTH = 10 * 1024 * 1024   # 10 MB limit

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

IMG_SIZE = (150, 150)   # Must match what the CNN was trained on


# ──────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def preprocess_image(file_path):
    """Resize, normalize and reshape image for the CNN model."""
    img = Image.open(file_path).convert('RGB')
    img = img.resize(IMG_SIZE)
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array


def get_risk_level(confidence, is_pneumonia):
    """Map prediction confidence + result to a human-readable risk level."""
    if is_pneumonia:
        # Pneumonia detected — higher confidence = more dangerous
        if confidence >= 0.70:
            return "High", "red"
        elif confidence >= 0.40:
            return "Medium", "orange"
        else:
            return "Low", "orange"
    else:
        # Normal result — higher confidence = safer = lower risk
        if confidence >= 0.70:
            return "Low", "green"
        elif confidence >= 0.40:
            return "Medium", "orange"
        else:
            return "High", "red"


def get_medical_tips(is_pneumonia, risk_level):
    """Return relevant medical guidance based on prediction result."""
    if is_pneumonia:
        tips = {
            "Low": [
                "Pneumonia indicators detected but confidence is low — consult a doctor for confirmation.",
                "Rest adequately and stay hydrated.",
                "Monitor symptoms closely — fever, cough, or breathing difficulty.",
                "Avoid smoking or exposure to pollutants.",
                "Maintain good hand hygiene to prevent spreading infection.",
            ],
            "Medium": [
                "Pneumonia detected with moderate confidence — seek medical attention promptly.",
                "A doctor may prescribe antibiotics if bacterial pneumonia is confirmed.",
                "Rest completely and avoid strenuous activities.",
                "Use prescribed medications and complete the full course.",
                "Monitor oxygen levels if possible; seek emergency care if breathing worsens.",
                "Stay hydrated with warm fluids.",
            ],
            "High": [
                "⚠️ Pneumonia strongly detected — seek immediate medical attention.",
                "Do NOT ignore symptoms — high-risk pneumonia can escalate quickly.",
                "Hospital-level care including IV antibiotics or oxygen therapy may be needed.",
                "Inform your doctor about any existing conditions (diabetes, heart disease, etc.).",
                "Avoid self-medication — professional diagnosis is critical.",
                "Keep emergency contacts accessible at all times.",
            ],
        }
    else:
        tips = {
            "Low": [
                "✅ Your X-ray appears normal with high confidence — great news!",
                "Maintain good hygiene: wash hands regularly.",
                "Stay up-to-date with flu and pneumococcal vaccinations.",
                "Practice deep-breathing exercises (5 min/day) for lung health.",
                "Avoid smoking and secondhand smoke exposure.",
                "Schedule annual respiratory check-ups if you're 60+ or have chronic conditions.",
            ],
            "Medium": [
                "Your X-ray appears normal but confidence is moderate — worth a check-up.",
                "Consult a doctor for a thorough examination to rule out early infection.",
                "Rest well and stay hydrated.",
                "Avoid cold environments and protect yourself from respiratory infections.",
                "Monitor for symptoms like persistent cough, fever, or shortness of breath.",
            ],
            "High": [
                "⚠️ No pneumonia detected but confidence is very low — results are uncertain.",
                "Professional medical review is strongly recommended — do not rely on this result alone.",
                "Do not delay seeing a doctor even if symptoms seem mild.",
                "Get a complete blood count (CBC) and clinical examination.",
                "Avoid self-diagnosis; let a radiologist review the X-ray in person.",
            ],
        }
    return tips.get(risk_level, tips["Low"])


def demo_predict():
    """Return a random demo result when no real model is available."""
    import random
    confidence = round(random.uniform(0.20, 0.95), 4)
    is_pneumonia = confidence > 0.5
    return is_pneumonia, confidence


# ──────────────────────────────────────────────
# Routes
# ──────────────────────────────────────────────
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    # 1. Check file presence
    if 'file' not in request.files:
        flash("No file part in the request. Please select an X-ray image.")
        return redirect(url_for('home'))

    file = request.files['file']

    if file.filename == '':
        flash("No file selected. Please upload a chest X-ray image.")
        return redirect(url_for('home'))

    if not allowed_file(file.filename):
        flash("Invalid file type. Please upload a JPG or PNG image.")
        return redirect(url_for('home'))

    # 2. Save uploaded file
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    # 3. Run prediction
    try:
        if model is not None:
            img_array = preprocess_image(file_path)
            prediction_prob = float(model.predict(img_array)[0][0])
            is_pneumonia = prediction_prob > 0.5
            confidence = prediction_prob if is_pneumonia else 1 - prediction_prob
        else:
            # Demo mode: simulate a result
            is_pneumonia, confidence = demo_predict()

        confidence_pct = round(confidence * 100, 2)
        risk_level, risk_color = get_risk_level(confidence, is_pneumonia)
        tips = get_medical_tips(is_pneumonia, risk_level)

        result_label = "PNEUMONIA DETECTED" if is_pneumonia else "NORMAL (No Pneumonia)"
        result_class = "positive" if is_pneumonia else "negative"

        demo_mode = model is None

        return render_template(
            'result.html',
            result_label=result_label,
            result_class=result_class,
            confidence=confidence_pct,
            risk_level=risk_level,
            risk_color=risk_color,
            tips=tips,
            filename=filename,
            demo_mode=demo_mode
        )

    except Exception as e:
        flash(f"Error during prediction: {str(e)}")
        return redirect(url_for('home'))


@app.errorhandler(413)
def too_large(e):
    flash("File is too large. Maximum allowed size is 10 MB.")
    return redirect(url_for('home'))


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    print("\n🚀 Pneumonia Detection App starting...")
    print(f"   Model path: {MODEL_PATH}")
    print(f"   Model loaded: {'Yes ✅' if model else 'No — Demo Mode ⚠️'}")
    print("   Open your browser at: http://127.0.0.1:5000\n")
    app.run(debug=True)
