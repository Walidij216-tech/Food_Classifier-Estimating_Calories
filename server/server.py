from flask import Flask, abort, request, jsonify, send_from_directory
import os
import util2
from flask_cors import CORS
from werkzeug.utils import secure_filename

app = Flask(__name__, static_folder='UI', template_folder='UI')
CORS(app)

# Répertoire d'upload
UPLOAD_FOLDER = 'C:\\Users\\Zaïneb\\Desktop\\food_cal\\server\\test_images'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return send_from_directory('UI', 'app.html')

@app.route('/classify_image', methods=['POST'])
def classify_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = secure_filename(file.filename)
    image_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(image_path)

    # Passer la liste des chemins d'images à predict_class
    result = util2.predict_class(util2.__model, [image_path], show=False)
    return jsonify(result[0])

@app.route('/class_image/<class_name>')
def class_image(class_name):
    # Liste des extensions d'image supportées
    supported_extensions = ['jpg', 'jpeg', 'png', 'jfif','webp']
    CLASS_IMAGES_FOLDER='C:\\Users\\Zaïneb\\Desktop\\food_cal\\server\\classe_image'
    for ext in supported_extensions:
        filename = f"{class_name}.{ext}"
        filepath = os.path.join(CLASS_IMAGES_FOLDER, filename)
        if os.path.exists(filepath):
            return send_from_directory(CLASS_IMAGES_FOLDER, filename)

    # Si aucun fichier n'a été trouvé, retourner une erreur 404
    abort(404, description="Image not found")


if __name__ == "__main__":
    print("Starting Python Flask Server For estimating food calories from Image Classification")
    util2.load_saved_artifacts()
    app.run(debug=True)
