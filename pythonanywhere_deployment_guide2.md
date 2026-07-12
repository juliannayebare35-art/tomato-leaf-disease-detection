# 🌿 PythonAnywhere Deployment Guide
### Tomato Leaf Care — Plant Disease Prediction App (Free Account)

---

## ✅ Before You Start (Do This on Your Local Computer)

Make sure you have already run the conversion script to generate `model.tflite`:
```powershell
python .\convert_to_tflite.py
```
You should see a file named `model.tflite` (≈14 MB) in your `PLANT_DISEASE_PROJECT` folder.

---

## STEP 1 — Zip Your Project Files

1. Open your `PLANT_DISEASE_PROJECT` folder on your desktop.
2. Select **only** these 5 items:
   - `leaf.py`
   - `model.tflite`
   - `requirements.txt`
   - `static` folder
   - `templates` folder
3. Right-click the selected items → **Send to** → **Compressed (zipped) folder**.
4. Name the zip file `Project.zip`.

> [!CAUTION]
> Do **NOT** include `model.h5`, `Tenv/`, `Dataset/`, `convert_to_tflite.py`, or any test scripts. These will waste your 512MB storage limit.

---

## STEP 2 — Upload the Zip to PythonAnywhere

1. Open your browser and go to: **https://www.pythonanywhere.com**
2. Log into your account.
3. Click the **Files** tab in the top navigation bar.
4. You will be in your home directory: `/home/yourusername/`
5. Click the **Upload a file** button on the right side of the page.
6. Browse to your desktop and select `Project.zip`.
7. Wait for the upload to finish (this may take a minute due to the model file).

---

## STEP 3 — Open a Bash Console

1. Click the **Consoles** tab in the top navigation bar.
2. Under **"Start a new console"**, click **Bash**.
3. A Linux terminal will open. This is where you will run all the following commands.

---

## STEP 4 — Extract the Zip File

In the Bash console, run these commands one by one:

```bash
# Unzip the project into a folder called PLANT_DISEASE_PROJECT
unzip Project.zip -d PLANT_DISEASE_PROJECT
```

Then verify all files are there:
```bash
cd PLANT_DISEASE_PROJECT
ls
```

You should see:
```
leaf.py  model.tflite  requirements.txt  static  templates
```

> [!NOTE]
> If after running `ls` you only see a folder called `Project` (and not the files directly), run these extra commands to move the files up one level:
> ```bash
> mv Project/* .
> rmdir Project
> ```
> Then run `ls` again to confirm the files are now visible.

---

## STEP 5 — Create the Upload Folder

The app needs a folder to store uploaded images. Create it:
```bash
mkdir -p static/upload
```

---

## STEP 6 — Create a Virtual Environment

Still in the Bash console, run:
```bash
mkvirtualenv --python=/usr/bin/python3.11 plant-env
```

Wait for it to finish. You will see `(plant-env)` appear at the start of your terminal prompt — this means the virtual environment is now active.

---

## STEP 7 — Install the Required Packages

With the virtual environment active, install only the packages needed:
```bash
pip install Flask numpy opencv-python-headless pillow tflite-runtime
```

> [!NOTE]
> This will take 2–3 minutes. Do **not** install `tensorflow` — it is too large for a free account. The app is already configured to use `tflite-runtime` automatically.

---

## STEP 8 — Set Up the Web App

1. Click the **Web** tab in the top navigation bar.
2. Click **Add a new web app**.
3. Click **Next**.
4. Select **Manual configuration** (scroll down past the framework options).
5. Select **Python 3.11**.
6. Click **Next** and then **Next** again to finish.

---

## STEP 9 — Configure the Web App Settings

You will now be on the Web app configuration page. Fill in these three fields:

### Source code:
```
/home/yourusername/PLANT_DISEASE_PROJECT
```

### Working directory:
```
/home/yourusername/PLANT_DISEASE_PROJECT
```

### Virtualenv:
```
/home/yourusername/.virtualenvs/plant-env
```

> [!IMPORTANT]
> Replace `yourusername` with your actual PythonAnywhere username in all three paths above.

---

## STEP 10 — Edit the WSGI Configuration File

1. On the Web tab, look for the **"Code"** section.
2. Click the link next to **"WSGI configuration file"** — it looks like:
   `/var/www/yourusername_pythonanywhere_com_wsgi.py`
3. A code editor will open. **Delete everything** inside it.
4. Paste this exact code:

```python
import sys
import os

# Path to your project
path = '/home/yourusername/PLANT_DISEASE_PROJECT'
if path not in sys.path:
    sys.path.insert(0, path)

# Set working directory
os.chdir(path)

# Import the Flask app from leaf.py
from leaf import app as application
```

5. Replace `yourusername` with your actual PythonAnywhere username.
6. Click **Save** in the top-right corner of the editor.

---

## STEP 11 — Map the Static Files

This makes your CSS, images, and Bootstrap files load faster.

1. Go back to the **Web** tab.
2. Scroll down to the **"Static files"** section.
3. Click the **Enter URL** and **Enter Path** boxes to add a new row:
   - **URL:** `/static/`
   - **Directory:** `/home/yourusername/PLANT_DISEASE_PROJECT/static`
4. Click the **checkmark/tick** to save the mapping.

---

## STEP 12 — Reload and Launch! 🚀

1. Scroll to the very top of the Web tab.
2. Click the big green button: **Reload yourusername.pythonanywhere.com**
3. Once it says "Reload complete", click the link to your website URL at the top.

**Your app is now live!** 🎉

---

## 🔍 Troubleshooting — If Something Goes Wrong

If you see an error page instead of your app, check the error log:

1. Go to the **Web** tab.
2. Scroll down to the **"Log files"** section.
3. Click **Error log** to see what went wrong.

### Common Issues & Fixes

| Problem | Fix |
|---|---|
| `ModuleNotFoundError: tflite_runtime` | Run `pip install tflite-runtime` in your Bash console with the virtual environment active |
| `FileNotFoundError: model.tflite` | Make sure `model.tflite` is directly inside `/home/yourusername/PLANT_DISEASE_PROJECT/`, not in a subfolder |
| Uploaded images fail to save | Run `mkdir -p /home/yourusername/PLANT_DISEASE_PROJECT/static/upload` in Bash |
| CSS/styles not loading | Double-check the static files mapping in Step 11 |
| `ImportError` on `cv2` | Run `pip install opencv-python-headless` in Bash |

---

## 📋 Quick Reference Checklist

- `[ ]` Ran `convert_to_tflite.py` locally and confirmed `model.tflite` exists
- `[ ]` Zipped only: `leaf.py`, `model.tflite`, `requirements.txt`, `static/`, `templates/`
- `[ ]` Uploaded `Project.zip` via the Files tab
- `[ ]` Extracted the zip in Bash: `unzip Project.zip -d PLANT_DISEASE_PROJECT`
- `[ ]` Created the upload folder: `mkdir -p static/upload`
- `[ ]` Created virtual environment: `mkvirtualenv --python=/usr/bin/python3.11 plant-env`
- `[ ]` Installed packages: `pip install Flask numpy opencv-python-headless pillow tflite-runtime`
- `[ ]` Added a Manual web app with Python 3.11
- `[ ]` Set Source code, Working directory, and Virtualenv paths
- `[ ]` Edited the WSGI file with the correct username
- `[ ]` Mapped `/static/` to the static folder
- `[ ]` Clicked Reload and confirmed the site loads
