# 🍅 Tomato Leaf Disease Detection Using Convolutional Neural Networks (CNNs)
##A case of Mubuku Irrigation Scheme, Nyambwamba Division, Kasese

A modern, deep learning-powered web application designed to help farmers, agronomists, and garden enthusiasts instantly diagnose tomato leaf diseases and receive actionable, science-backed organic and chemical treatment recommendations.

![Deep Learning](https://img.shields.io/badge/Deep%20Learning-TensorFlow%20%2F%20Keras-orange)
![Computer Vision](https://img.shields.io/badge/Computer%20Vision-OpenCV-blue)
![Web Framework](https://img.shields.io/badge/Backend-Flask-green)
![Deployment](https://img.shields.io/badge/Deployment-PythonAnywhere-yellow)
![Status](https://img.shields.io/badge/Status-Production--Ready-brightgreen)

---
##✨️Problem statement
Tomato farmers in the Mubuku Irrigation Scheme rely mainly on personal experience or physically consulting agricultural extension officers to identify leaf diseases. This approach is slow, inconsistent, and often inaccessible, since extension officers are few and not always available in time — leading to delayed diagnosis, misdiagnosis, and avoidable crop losses.
## 🌟 Key Features

1. **Instant AI Diagnosis:** Upload a close-up image of a tomato leaf, and the custom deep learning model classifies it into one of 10 categories (9 diseases + healthy state) in milliseconds.
2. **Robust Out-of-Distribution (OOD) Verification:** Integrated multi-stage safety filters prevent false positives from non-leaf images or unrelated content:
   * **Color Check (HSV):** Uses OpenCV to ensure the image contains at least 5% foliage tones (greens, yellows, and browns).
   * **Feature Activation Check:** Inspects the L2 Norm, Mean, and Max activation values at the neural network's penultimate layer to mathematically reject out-of-distribution patterns (e.g., rejecting an image of a green car or animal).
3. **Actionable Treatments:** Provides detailed, organic, and chemical treatment routines for every diagnosed disease.
4. **Modern Glassmorphism UI:** A premium user interface built with frosted-glass containers, side-by-side image comparisons, and fully responsive layouts.
5. **Resource-Optimized Fallback:** Native support for `tflite-runtime` allows the application to automatically fall back to TensorFlow Lite inference if full TensorFlow is not installed, enabling deployment on low-memory servers (like the PythonAnywhere Free Tier).

---

## 🛠️ Technical Architecture

The following diagram illustrates the application's processing flow and prediction pipeline:

```mermaid
graph TD
    A[User Browser] -->|POST Upload Image| B[Flask Server]
    B -->|Preprocess to 128x128| C[OOD Detection Pipeline]
    C -->|HSV Color Check < 5%| D[Reject: unrecognized.html]
    C -->|Penultimate Layer L2 Norm Check| D
    C -->|Passes All Checks| E{TensorFlow Installed?}
    E -->|Yes| F[Predict using model.h5]
    E -->|No| G[Predict using model.tflite]
    F -->|Output Prediction| H[Render Results Page]
    G -->|Output Prediction| H
    H -->|Display Diagnosis & Treatments| A
```

### Stack Detail
* **Frontend:** HTML5, CSS3 (Custom Glassmorphism CSS design system in `glass.css`), Bootstrap 4.5.1, Vanilla JavaScript.
<img width="1897" height="909" alt="image" src="https://github.com/user-attachments/assets/8cbc5e52-75f3-453e-800b-9dd1922f46f2" />
<img width="956" height="455" alt="image" src="https://github.com/user-attachments/assets/af2d57d3-e713-4ce8-a373-49cac9aa6ff7" />
<img width="951" height="393" alt="image" src="https://github.com/user-attachments/assets/e3de2293-5b9d-4182-ad85-048fc2b5ca89" />

* **Backend:** Python 3, Flask framework.
* **Computer Vision:** OpenCV (`cv2`) for HSV color masking and foliage verification.
* **Deep Learning Inference:**
  * **Primary:** TensorFlow/Keras (`model.h5` sequential CNN).
  * **Lightweight Fallback:** TensorFlow Lite (`model.tflite` quantized model) for resource-constrained environments.

---

## 📋 Supported Disease Categories

The neural network is trained to identify the following conditions:

| Diagnosis Label | Status | Example Treatment Approach |
| :--- | :--- | :--- |
| **Healthy and Fresh** | Clean Foliage | N/A (Maintain regular watering & soil health) |
| **Bacteria Spot Disease** | Infected | Copper-based bactericide sprays |
| **Early Blight Disease** | Infected | Liquid Copper / Organic bio-fungicides |
| **Late Blight Disease** | Infected | Immediate organic/chemical fungicide intervention |
| **Leaf Mold Disease** | Infected | Pruning, drip irrigation, increasing airflow |
| **Septoria Leaf Spot** | Infected | Potassium bicarbonate, Chlorothalonil |
| **Target Spot Disease** | Infected | Mancozeb, copper oxychloride |
| **Tomato Mosaic Virus** | Infected | Eradication of infected plants (Preventative tools only) |
| **Yellow Leaf Curl Virus** | Infected | Insecticidal soaps for whiteflies, Neem oil |
| **Two Spotted Spider Mite** | Infected | Bifenazate, selective miticides, predatory mites |

---

## 📂 Directory Structure

```text
├── leaf.py                             # Core Flask application and prediction logic
├── requirements.txt                    # Python dependencies
├── .gitignore                          # Excludes datasets, environments, and cache files
├── pythonanywhere_deployment_guide.md  # Detailed cloud deployment guide (Quick)
├── pythonanywhere_deployment_guide2.md # Complete step-by-step deployment checklist
├── convert_to_tflite.py                # Model conversion script (h5 -> tflite)
├── rebuild_templates.py                # Utility to maintain HTML layouts
├── verify_routing.py                   # Automated routing and prediction validation tests
├── model.h5                            # Full TensorFlow Keras model (44MB)
├── model.tflite                        # Quantized TF Lite model (14.8MB)
├── my_model_weights.h5                 # Keras model weights (14.8MB)
├── model1.json                         # Model architecture in JSON format
├── extracted_details.json              # Extracted disease metadata
├── static/
│   ├── css/                            # Bootstrap and Custom Glassmorphism styles
│   ├── images/                         # UI images and disease reference illustrations
│   └── upload/                         # Temporary folder for user-uploaded leaf images
└── templates/
    ├── index.html                      # Landing & upload interface
    ├── unrecognized.html               # OOD Rejection error page
    └── Tomato-*.html                   # 10 specific disease diagnosis result pages
```

---

## 🚀 Running Locally

### Prerequisites
Make sure Python 3.9 - 3.11 is installed on your machine.

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/tomato-leaf-disease-detection.git
   cd tomato-leaf-disease-detection
   ```

2. **Create a Virtual Environment:**
   * **Windows:**
     ```powershell
     python -m venv venv
     .\venv\Scripts\activate
     ```
   * **macOS/Linux:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the Web Server:**
   ```bash
   python leaf.py
   ```

5. **Access the Interface:**
   Open your browser and navigate to `http://127.0.0.1:5001`.

6. **Run Verification Tests:**
   Ensure all prediction and OOD paths are working properly by executing:
   ```bash
   python verify_routing.py
   ```

---

## ☁️ Deployment (PythonAnywhere)

Deploying deep learning models to free cloud tiers can be challenging due to disk space limits (e.g., 512MB on PythonAnywhere). 

This project solves this by using a **TFLite fallback mechanism** inside `leaf.py`. By running with `tflite-runtime` and `opencv-python-headless`, the app avoids loading the heavy `tensorflow` library, reducing memory usage and staying well under disk limits.

* For a quick guide, read the [PythonAnywhere Deployment Guide](pythonanywhere_deployment_guide.md).
* For a comprehensive checklist, follow the [Detailed Deployment Guide](pythonanywhere_deployment_guide2.md).

---

## 🧠 Model Training & Deep Learning Pipeline

The system is powered by a custom Convolutional Neural Network (CNN) built sequentially using Keras and TensorFlow. 

### Model Architecture
1. **Input Layer:** Accepts normalized images of size $128 \times 128 \times 3$ (RGB format).
2. **Convolutional Block 1:** 
   * `Conv2D` layer with 32 filters, a $3\times3$ kernel, and ReLU activation.
   * `MaxPooling2D` layer with a $2\times2$ pool size to reduce spatial dimensions.
3. **Convolutional Block 2:** 
   * `Conv2D` layer with 32 filters, a $3\times3$ kernel, and ReLU activation.
   * `MaxPooling2D` layer with a $2\times2$ pool size.
4. **Flattening Layer:** Converts the 2D feature maps into a 1D vector.
5. **Dense Block:** 
   * Fully connected `Dense` layer with 128 neurons and ReLU activation.
   * Penultimate feature extraction point (used for OOD activation checks).
6. **Output Layer:** Fully connected `Dense` layer with 10 outputs using Sigmoid activation (compiled with `categorical_crossentropy` loss and Adam optimizer).

### Training Configuration
* **Optimization Algorithm:** Adam
* **Loss Function:** Categorical Crossentropy
* **Epochs:** 50
* **Data Augmentation:** Real-time training augmentation including scaling, shear range (0.2), zoom range (0.2), and horizontal flips.

---

## 🛡️ Out-of-Distribution (OOD) Pipeline & Calibration

To prevent the model from confidently classifying unrelated images (such as cars, pets, or household objects) as plant diseases, we implement a multi-stage validation pipeline:

### 1. Color Masking (HSV Space)
Images are converted to the Hue-Saturation-Value (HSV) color space to check for organic foliage tones. The mask filters for:
* **Greens:** $Hue \in [35, 85]$
* **Yellows & Browns:** $Hue \in [10, 35]$

If the combined area of green, yellow, and brown pixels accounts for **less than 5%** of the total image area, the image is immediately flagged and rejected as non-foliage.

### 2. Penultimate Feature Activation Checking
For images that contain green/yellow elements but are not leaves (such as a green car), the app inspects the feature map activations of the neural network's final hidden dense layer. 

We calibrated the network using test sets to determine the boundaries for in-distribution leaf images. Out-of-distribution (OOD) images trigger abnormally high feature values. The validation thresholds are:
* **L2 Norm Threshold:** Reject if $> 52.0$
* **Max Activation:** Reject if $> 21.0$
* **Mean Activation:** Reject if $> 2.0$

If any threshold is exceeded, the image is routed to `unrecognized.html`.

---

## 🗺️ Project Roadmap

- [ ] **In-Browser Camera Capture:** Allow users to capture leaf photos directly via webcam/mobile camera.
- [ ] **Multi-Crop Expansion:** Extend the model classes to diagnose diseases in potatoes, corn, and bell peppers.
- [ ] **Edge Processing (TensorFlow.js):** Compile the lightweight TFLite model to TF.js to perform disease predictions entirely client-side without server dependencies.

---

## ❔ FAQ

**Q: Why does the project use `opencv-python-headless` instead of standard `opencv-python`?**  
**A:** Headless OpenCV is designed specifically for server environments (like Docker containers and PythonAnywhere). It does not require GUI dependencies (like GTK or Qt) which often crash cloud web servers.

**Q: Why does the app support both `model.h5` and `model.tflite`?**  
**A:** `model.h5` is the full TensorFlow model used for local development and prediction accuracy. `model.tflite` is a lightweight, compressed version of the model that runs with `tflite-runtime`. This is critical for deployment on low-memory servers (such as PythonAnywhere's 512MB free tier), preventing memory overflow crashes.

**Q: How do I retrain the model with my own dataset?**  
**A:** Place your images inside the `Dataset/train` and `Dataset/val` folders, run `python Training.py`, and run `python convert_to_tflite.py` to regenerate the lightweight model weights.

---

## 📝 License & Open Source

This project is open-source. Feel free to use, modify, and distribute it for educational, commercial, or research purposes.
