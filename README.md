# 🫁 Pneumonia Detection Using Deep Learning

A web-based AI application that detects pneumonia from chest X-ray images
using a Convolutional Neural Network (CNN), built with Python and Flask.

---

## 📌 About The Project:
Pneumonia is a serious respiratory disease that requires early and accurate
diagnosis. This project presents an automated pneumonia detection system using
deep learning techniques applied to chest X-ray images.

---

Problem:
- Pneumonia detection from chest X-rays is time-consuming
- Manual diagnosis can be error-prone

Solution:
- Built a CNN-based model to classify X-rays
- Integrated into Flask web app

Results:
- Accuracy: 80%
- Binary classification: Normal vs Pneumonia

Screenshots:
<img width="1920" height="827" alt="Pneumodetect 1" src="https://github.com/user-attachments/assets/ee56e52e-45c4-44ee-8e6b-180fd29d6f48" />
<img width="1920" height="829" alt="Pneumodetect 2" src="https://github.com/user-attachments/assets/9a4c9fd5-d3b3-4563-b497-f411202ad2ea" />
<img width="1920" height="827" alt="Pneumodetect 3" src="https://github.com/user-attachments/assets/cf9c2a5e-f8db-45f7-9067-b4d10c2bbead" />
<img width="1920" height="826" alt="Pneumodetect 4" src="https://github.com/user-attachments/assets/15474291-8590-4268-ae57-3a927b7544a7" />

---

The system:
- Accepts chest X-ray images uploaded by the user
- Runs them through a trained CNN model
- Classifies the image as **Normal** or **Pneumonia**
- Assigns a **Risk Level** — Low / Medium / High
- Provides **Medical Guidance** and precautionary tips

---

## 🖥️ Screenshots:
> Homepage — Upload your chest X-ray  
> Result Page — Prediction + Risk Level + Medical Tips

---

## 🧠 How The System Works:
1. User uploads a chest X-ray image (JPG/PNG)
2. Image is resized to 150×150 and normalized
3. Passed through a 4-block CNN model
4. Model outputs a probability score (0 to 1)
5. Score > 0.5 → Pneumonia | Score ≤ 0.5 → Normal
6. Risk level assigned based on confidence percentage
7. Result displayed with medical guidance

---

## 🛠️ Tech Stack:

| Layer             | Technology              |
|-------------------|-------------------------|
| Backend           | Python 3, Flask         |
| Deep Learning     | TensorFlow & Keras      |
| Image Processing  | Pillow, NumPy           |
| Frontend          | HTML5, CSS3, JavaScript |
| Model Format      | HDF5 (.h5)              |
| IDE               | Visual Studio Code      |

---

## 📁 Project Structure:
pneumonia_detection/
├── app.py               ← Flask backend
├── train_model.py       ← CNN training script
├── requirements.txt     ← Dependencies
├── model/               ← Trained model stored here
├── templates/           ← HTML pages
│   ├── index.html
│   └── result.html
├── static/
│   ├── css/style.css
│   └── js/main.js
└── uploads/             ← Temporary image uploads

---

## ✅ Features:
- Drag & drop or click-to-upload X-ray images
- Real-time image preview before submission
- File type and size validation
- CNN-based binary classification
- Confidence percentage display
- Risk level: Low / Medium / High
- Personalized medical guidance tips
- Fully responsive design (mobile friendly)
- Error handling for invalid uploads

---

## 📊 Model Details

| Parameter         | Value                       |
|-------------------|-----------------------------|
| Architecture      | Custom CNN (4 Conv blocks)  |
| Input Size        | 150 × 150 × 3 (RGB)         |
| Output            | Binary (Normal / Pneumonia) |
| Training Images   | 80 (augmented)              |
| Validation Images | 10                          |
| Test Images       | 10                          |
| Loss Function     | Binary Crossentropy         |
| Epochs            | 30                          |

> For production-level accuracy, retrain using the full Kaggle dataset(link: https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia/data)
> (~5,800 images). This project uses a sample dataset for demonstration.

---

## ⚠️ Disclaimer:
This application is developed for **academic and educational purposes only**.
It is **not a medical device** and should **not** be used for actual clinical
diagnosis. Always consult a qualified medical professional for medical advice.

---

## 👩‍💻 Developed By:

*Sailaja*  
B.Tech — Computer Science & Engineering  
Rishi MS Institute of Engineering & Technology for Women  
Batch: 2022–2026
