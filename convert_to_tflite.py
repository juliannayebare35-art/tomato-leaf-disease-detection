import tensorflow as tf
import os

print("Loading Keras model...")
base_model = tf.keras.models.load_model('model.h5')

# Reconstruct as a Functional Model to bypass Keras 3 Sequential output limitations
inputs = tf.keras.Input(shape=(128, 128, 3))
x = inputs
penultimate_output = None
for i, layer in enumerate(base_model.layers):
    x = layer(x)
    if i == len(base_model.layers) - 2:
        penultimate_output = x

multi_output_model = tf.keras.Model(inputs=inputs, outputs=[x, penultimate_output])

print("Converting model to TensorFlow Lite...")
converter = tf.lite.TFLiteConverter.from_keras_model(multi_output_model)
tflite_model = converter.convert()

tflite_path = 'model.tflite'
with open(tflite_path, 'wb') as f:
    f.write(tflite_model)

print(f"Success! Saved TensorFlow Lite model to: {tflite_path}")
print(f"Original size: {os.path.getsize('model.h5')/1024/1024:.2f} MB")
print(f"TFLite size: {os.path.getsize(tflite_path)/1024/1024:.2f} MB")
