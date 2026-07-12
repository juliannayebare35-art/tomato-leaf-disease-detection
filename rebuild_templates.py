import os
import re

html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tomato Leaf Disease Prediction</title>
    <!-- Local Bootstrap CSS -->
    <link rel="stylesheet" href="{{ url_for('static', filename='css/bootstrap.min.css') }}">
    <!-- Shared Glassmorphism CSS -->
    <link rel="stylesheet" href="{{ url_for('static', filename='css/glass.css') }}">
</head>
<body background="{{ url_for('static', filename='images/Background.jpg') }}">
    <nav class="top-nav">
        <a href="/" class="nav-brand">
            <span class="nav-brand-icon">🌱</span>
            <div>
                <span class="nav-brand-text">Tomato Leaf Disease Prediction</span>
            </div>
        </a>
        <a href="/" class="nav-back-btn">
            ← Scan Another Leaf
        </a>
    </nav>

    <div class="page-wrapper" style="padding-top: 40px;">
        <div class="container">
            <div class="row">
                <div class="col-md-5">
                    <div class="image-frame">
                        <div class="image-card">
                            <img src="__IMAGE_SRC__" alt="Leaf Image">
                            <div class="image-card-label">Analyzed Leaf</div>
                        </div>
                    </div>
                </div>
                <div class="col-md-7 mt-4 mt-md-0">
                    <div class="result-panel">
                        <div class="result-status-banner __STATUS_CLASS__">
                            <div class="result-status-icon">__STATUS_ICON__</div>
                            <div class="result-status-text">
                                <h2>{{pred_output}}</h2>
                                <p>__STATUS_SUBTITLE__</p>
                            </div>
                        </div>
                        <div class="result-body">
                            <div class="info-block __INFO_CLASS__">
                                <div class="info-block-title">
                                    <span>⚕️</span> Treatment Plan
                                </div>
                                <p>__TREATMENT_TEXT__</p>
                            </div>
                            <div class="action-area mt-4">
                                <a href="/" class="btn-primary-glass">🔍 Diagnose Another</a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""

unrecognized_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tomato Leaf Disease Prediction</title>
    <!-- Local Bootstrap CSS -->
    <link rel="stylesheet" href="{{ url_for('static', filename='css/bootstrap.min.css') }}">
    <!-- Shared Glassmorphism CSS -->
    <link rel="stylesheet" href="{{ url_for('static', filename='css/glass.css') }}">
</head>
<body background="{{ url_for('static', filename='images/Background.jpg') }}">
    <nav class="top-nav">
        <a href="/" class="nav-brand">
            <span class="nav-brand-icon">🌱</span>
            <div>
                <span class="nav-brand-text">Tomato Leaf Disease Prediction</span>
            </div>
        </a>
        <a href="/" class="nav-back-btn">
            ← Scan Another Leaf
        </a>
    </nav>

    <div class="page-wrapper" style="padding-top: 40px;">
        <div class="container d-flex justify-content-center">
            <div class="col-md-8 mt-4">
                <div class="result-panel text-center">
                    <div class="result-status-banner warning" style="justify-content: center;">
                        <div class="result-status-icon">⚠️</div>
                        <div class="result-status-text text-center">
                            <h2>Unrecognized Image</h2>
                            <p>Please upload a clear image of a tomato leaf</p>
                        </div>
                    </div>
                    <div class="result-body">
                        <div class="info-block yellow">
                            <p>The uploaded image does not appear to be a tomato leaf, or it is too blurry to be diagnosed correctly. Please take a clear close-up photo of the affected tomato leaf and try again.</p>
                        </div>
                        <div class="action-area mt-4 d-flex justify-content-center">
                            <a href="/" class="btn-primary-glass">🔍 Upload Another Image</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""

folder = r"c:\Users\user\Desktop\PLANT_DISEASE_PROJECT\templates"
for f in os.listdir(folder):
    if not f.startswith("Tomato") or not f.endswith(".html"):
        continue
    
    path = os.path.join(folder, f)
    with open(path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Extract image src
    img_match = re.search(r'<img src="([^"]+)"', content)
    if not img_match:
        img_match = re.search(r"<img src='([^']+)'", content)
    
    if img_match:
        img_src = img_match.group(1)
    else:
        img_src = "{{ url_for('static', filename='images/Tomato___healthy .JPG') }}"
        
    # Extract treatment text
    treatment_text = ""
    treatment_match = re.search(r'<h4><b> Treatment : </b> </h4>\s*<h6>(.*?)</h6>', content, re.DOTALL)
    if treatment_match:
        treatment_text = treatment_match.group(1).strip()
        treatment_text = treatment_text.replace('</br>', '<br>').strip()
    else:
        # Check if healthy
        healthy_match = re.search(r'<h4><b> There is no disease on the Tomato leaf. </b> </h4>', content)
        if healthy_match:
            treatment_text = "No treatment necessary! Your tomato plant is perfectly healthy. Continue with standard care and watering."
        else:
            treatment_text = "Please follow standard treatment guidelines for this condition."
            
    # Determine status colors
    is_healthy = "healthy" in f.lower()
    if is_healthy:
        status_class = "healthy"
        status_icon = "✅"
        status_subtitle = "Leaf is healthy"
        info_class = "green"
    else:
        status_class = "disease"
        status_icon = "⚠️"
        status_subtitle = "Disease Detected"
        info_class = "red"
        
    new_content = html_template.replace("__IMAGE_SRC__", img_src)
    new_content = new_content.replace("__STATUS_CLASS__", status_class)
    new_content = new_content.replace("__STATUS_ICON__", status_icon)
    new_content = new_content.replace("__STATUS_SUBTITLE__", status_subtitle)
    new_content = new_content.replace("__INFO_CLASS__", info_class)
    new_content = new_content.replace("__TREATMENT_TEXT__", treatment_text)
    
    with open(path, 'w', encoding='utf-8') as file:
        file.write(new_content)

# write unrecognized.html
with open(os.path.join(folder, 'unrecognized.html'), 'w', encoding='utf-8') as file:
    file.write(unrecognized_template)
