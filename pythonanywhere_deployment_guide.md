# PythonAnywhere Deployment Guide

This guide provides a clean, step-by-step path to successfully deploying this Plant Disease Prediction project on the PythonAnywhere Free Tier. 

The PythonAnywhere Free Tier has strict disk space (512MB) and memory limits, so we use a **lightweight fallback mechanism** (TFLite and headless OpenCV) instead of the standard, heavy TensorFlow library.

---

## Deployment Steps

### Step 1: Upload Only Necessary Files
To stay under the 512MB disk limit, only upload what the web app strictly needs to run.
1. Go to the **Files** tab on PythonAnywhere and open your project folder (`/home/YourUsername/PLANT_DISEASE_PROJECT`).
2. Upload your code (`leaf.py`, `templates/`, `static/`).
3. Upload the lightweight model: `model.tflite`.
4. **DO NOT** upload `model.h5` (~44MB) or any project `.zip` files, as these will quickly exhaust your disk quota.

### Step 2: Create a Virtual Environment
Isolate your dependencies from the global system Python.
1. Open a **Bash console** on PythonAnywhere.
2. Create a virtual environment (replace `plant-env` with your preferred name):
   ```bash
   mkvirtualenv plant-env --python=python3.10
   ```

### Step 3: Install Lightweight Dependencies
Run the following commands sequentially in your virtual environment. We use specific versions and flags to avoid dependency conflicts and save disk space.
```bash
pip cache purge
pip install --no-cache-dir "numpy<2" opencv-python-headless==4.9.0.80 tflite-runtime Flask Pillow werkzeug
```

### Step 4: Link Virtual Environment & WSGI
Tell the web server where to find your code and your installed packages.
1. Go to the **Web** tab on the PythonAnywhere dashboard.
2. Scroll down to the **Virtualenv** section. Enter the absolute path to your environment (e.g., `/home/YourUsername/.virtualenvs/plant-env`) and save it.
3. Click the **WSGI configuration file** link. Scroll to the bottom and configure it to import your Flask instance:
   ```python
   import sys

   # The absolute path to your project folder
   path = '/home/YourUsername/PLANT_DISEASE_PROJECT'
   if path not in sys.path:
       sys.path.append(path)

   # Import the Flask instance 'app' from leaf.py
   from leaf import app as application
   ```

### Step 5: Launch
1. Go back to the **Web** tab and click the big green **Reload** button at the top.
2. Open your website link!

---

## Troubleshooting Guide

If the site fails to load or the installation fails, consult these common issues.

### 1. Web Page shows "Unhandled Exception"
**Symptom**: You open the site and see a generic error page.
**Diagnosis**: The app crashed during startup. Scroll to the bottom of the **Web** tab and click the `error.log` link. Look at the very last lines of the log to find the specific error.

### 2. error.log shows "ModuleNotFoundError: No module named 'tensorflow'"
**Symptom**: Your `error.log` shows it crashing on the `try:` block trying to import tensorflow.
**Fix**: The web server is not using your virtual environment and is falling back to the default System Python. Go to the **Web** tab, enter the exact path to your virtual environment in the Virtualenv section, and hit Reload.

### 3. Installation fails with "Disk quota exceeded"
**Symptom**: Pip crashes during installation saying you are out of space.
**Fix**: 
1. Delete unused heavy files in the Files tab (`model.h5`, `.zip` archives).
2. Run `pip cache purge` in the console to wipe temporary pip files.
3. Ensure you add the `--no-cache-dir` flag to your pip install command.

### 4. Crash running leaf.py: "AttributeError: _ARRAY_API not found"
**Symptom**: `numpy.core.multiarray failed to import` when testing the script.
**Fix**: `tflite-runtime` is incompatible with the new NumPy 2.0. You must downgrade NumPy. Run:
```bash
pip install "numpy<2"
```

### 5. Dependency conflict: "opencv-python-headless requires numpy>=2"
**Symptom**: When trying to downgrade NumPy, pip complains that OpenCV requires the new NumPy 2.0.
**Fix**: You must install a slightly older version of OpenCV that is compatible with NumPy 1.x. Run:
```bash
pip install opencv-python-headless==4.9.0.80
```
