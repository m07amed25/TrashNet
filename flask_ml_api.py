from flask import Flask, request, jsonify
from flask_cors import CORS
from tensorflow.keras.models import load_model  #type: ignore
from tensorflow.keras.preprocessing import image    #type: ignore
import numpy as np
import tensorflow as tf
import os

app = Flask(__name__)

CORS(app, resources={
    r"/predict": {
        "origins": "*", 
        "methods": ["POST"],
        "allow_headers": ["Content-Type"]
    }
})

model = load_model('best_model.h5')

class_names = ["cardboard", "glass", "metal", "paper", "plastic", "trash"]

def preprocess_image(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = tf.keras.applications.efficientnet.preprocess_input(img_array)
    return img_array

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file found in the request'}), 400

    img_file = request.files['image']
    if img_file.filename == '':
        return jsonify({'error': 'Empty filename'}), 400

    try:
        img_path = os.path.join("temp", img_file.filename)
        os.makedirs("temp", exist_ok=True)
        img_file.save(img_path)

        img_array = preprocess_image(img_path)
        predictions = model.predict(img_array)
        predicted_class = np.argmax(predictions, axis=1)
        class_name = class_names[predicted_class[0]]

        os.remove(img_path)

        return jsonify({'predicted_class': class_name})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
