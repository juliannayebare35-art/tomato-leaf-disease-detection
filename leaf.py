#Import necessary libraries
from flask import Flask, render_template, request

import numpy as np
import os
import cv2

try:
    from tensorflow.keras.preprocessing.image import load_img
    from tensorflow.keras.preprocessing.image import img_to_array
    from tensorflow.keras.models import load_model
    HAS_TENSORFLOW = True
except ImportError:
    HAS_TENSORFLOW = False
    import tflite_runtime.interpreter as tflite
    from PIL import Image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if HAS_TENSORFLOW:
    filepath = os.path.join(BASE_DIR, 'model.h5')
    model = load_model(filepath)
    print(model)
    print("TensorFlow Model Loaded Successfully")
else:
    filepath = os.path.join(BASE_DIR, 'model.tflite')
    interpreter = tflite.Interpreter(model_path=filepath)
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    print("TFLite Model Loaded Successfully")

def is_leaf_color_present(image_path):
    img = cv2.imread(image_path)
    if img is None:
        return False
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # Green: Hue 35-85, Sat 30-255, Val 30-255
    lower_green = np.array([35, 30, 30])
    upper_green = np.array([85, 255, 255])
    # Yellow/Brown: Hue 10-35, Sat 30-255, Val 30-255
    lower_yellow_brown = np.array([10, 30, 30])
    upper_yellow_brown = np.array([35, 255, 255])
    
    mask_green = cv2.inRange(hsv, lower_green, upper_green)
    mask_yellow = cv2.inRange(hsv, lower_yellow_brown, upper_yellow_brown)
    
    total_pixels = img.shape[0] * img.shape[1]
    leaf_pixels = np.sum(mask_green > 0) + np.sum(mask_yellow > 0)
    leaf_pct = leaf_pixels / total_pixels
    print(f"@@ Color Check: Green/Yellow/Brown percentage = {leaf_pct:.2%}")
    return leaf_pct >= 0.05

def pred_tomato_dieas(tomato_plant):
  # 1. Color Check
  try:
      if not is_leaf_color_present(tomato_plant):
          print("@@ Image rejected by color check: not enough green/yellow/brown colors.")
          return "Unrecognized Image", 'unrecognized.html'
  except Exception as e:
      print("Error in color check:", e)

  if HAS_TENSORFLOW:
      test_image = load_img(tomato_plant, target_size = (128, 128)) # load image 
      print("@@ Got Image for prediction")
      test_image = img_to_array(test_image)/255 # convert image to np array and normalize
      test_image_dims = np.expand_dims(test_image, axis = 0) # change dimention 3D to 4D

      # 2. CNN Feature activation check (OOD check)
      try:
          x = test_image_dims
          for layer in model.layers[:-1]:
              x = layer(x)
          
          import tensorflow as tf
          if hasattr(x, 'numpy'):
              feats = x.numpy()[0]
          else:
              sess = tf.compat.v1.keras.backend.get_session()
              feats = sess.run(x)[0]
              
          norm = np.linalg.norm(feats)
          max_act = np.max(feats)
          mean_act = np.mean(feats)
          print(f"@@ Feature Norm Check: L2 Norm = {norm:.4f}, Mean = {mean_act:.4f}, Max = {max_act:.4f}")
          
          # Threshold checks based on calibration test
          if norm > 52.0 or max_act > 21.0 or mean_act > 2.0:
              print("@@ Image rejected by feature norm check: out of distribution.")
              return "Unrecognized Image", 'unrecognized.html'
      except Exception as e:
          print("Error in feature norm check:", e)

      result = model.predict(test_image_dims) # predict diseased palnt or not
      print('@@ Raw result = ', result)
  else:
      # PIL open and resize, normalize
      img = Image.open(tomato_plant).resize((128, 128))
      print("@@ Got Image for prediction (TFLite)")
      test_image = np.array(img, dtype=np.float32) / 255.0
      test_image_dims = np.expand_dims(test_image, axis = 0)

      # Run prediction using TFLite Interpreter
      interpreter.set_tensor(input_details[0]['index'], test_image_dims)
      interpreter.invoke()

      out0 = interpreter.get_tensor(output_details[0]['index'])
      out1 = interpreter.get_tensor(output_details[1]['index'])

      # Map classification output vs. penultimate features by shape
      if out0.shape[1] == 10:
          result = out0
          feats = out1[0]
      else:
          result = out1
          feats = out0[0]

      norm = np.linalg.norm(feats)
      max_act = np.max(feats)
      mean_act = np.mean(feats)
      print(f"@@ Feature Norm Check (TFLite): L2 Norm = {norm:.4f}, Mean = {mean_act:.4f}, Max = {max_act:.4f}")

      # Threshold checks based on calibration test
      if norm > 52.0 or max_act > 21.0 or mean_act > 2.0:
          print("@@ Image rejected by feature norm check (TFLite): out of distribution.")
          return "Unrecognized Image", 'unrecognized.html'

      print('@@ Raw result (TFLite) = ', result)
  
  pred = np.argmax(result, axis=1)
  print(pred)
  if pred==0:
      return "Tomato - Bacteria Spot Disease", 'Tomato-Bacteria Spot.html'
       
  elif pred==1:
      return "Tomato - Early Blight Disease", 'Tomato-Early_Blight.html'
        
  elif pred==2:
      return "Tomato - Healthy and Fresh", 'Tomato-Healthy.html'
        
  elif pred==3:
      return "Tomato - Late Blight Disease", 'Tomato - Late_blight.html'
       
  elif pred==4:
      return "Tomato - Leaf Mold Disease", 'Tomato - Leaf_Mold.html'
        
  elif pred==5:
      return "Tomato - Septoria Leaf Spot Disease", 'Tomato - Septoria_leaf_spot.html'
        
  elif pred==6:
      return "Tomato - Target Spot Disease", 'Tomato - Target_Spot.html'
        
  elif pred==7:
      return "Tomato - Tomoato Yellow Leaf Curl Virus Disease", 'Tomato - Tomato_Yellow_Leaf_Curl_Virus.html'
  elif pred==8:
      return "Tomato - Tomato Mosaic Virus Disease", 'Tomato - Tomato_mosaic_virus.html'
        
  elif pred==9:
      return "Tomato - Two Spotted Spider Mite Disease", 'Tomato - Two-spotted_spider_mite.html'

    

# Create flask instance
app = Flask(__name__)

# render index.html page
@app.route("/", methods=['GET', 'POST'])
def home():
        return render_template('index.html')
    
 
# get input image from client then predict class and render respective .html page for solution
@app.route("/predict", methods = ['GET','POST'])
def predict():
     if request.method == 'POST':
        file = request.files['image'] # fet input
        filename = file.filename        
        print("@@ Input posted = ", filename)
        
        file_path = os.path.join(BASE_DIR, 'static', 'upload', filename)
        file.save(file_path)

        print("@@ Predicting class......")
        pred, output_page = pred_tomato_dieas(tomato_plant=file_path)
              
        return render_template(output_page, pred_output = pred, user_image = filename)
    
# For local system & cloud
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001) 


    
    
