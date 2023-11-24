from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from ultralytics import YOLO
from PIL import Image
from base64 import encodebytes
import os
import io

os.makedirs("static/img/input", exist_ok=True)

UPLOAD_FOLDER = "/static/img/input"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
cors = CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CORS_HEADERS'] = 'Content-Type'

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# https://docs.ultralytics.com/modes/predict/#introduction
def yolo_process(image_path):
    weight = 'best.pt'
    model = YOLO(weight)
    results = model.predict(image_path, project="output", save=True, exist_ok=True)

    # cwd = os.getcwd()
    # filename_arr = filename.split('.')
    # filename_no_ext = ""
    # for i in range(len(filename_arr)):
    #     if i == len(filename_arr) - 1:
    #         break
    #     filename_no_ext += filename_arr[i]

    # save_path = cwd + "/output/" + filename_no_ext + ".txt"
    # results[0].save_txt(save_path, save_conf=True)
    # for result in results:
    #     print(result.boxes)

@app.route("/predict", methods=["GET"])
def predict():
    filename = secure_filename(request.args.get('fileName'))
    cwd = os.getcwd()
    save_path = cwd + app.config['UPLOAD_FOLDER'] + "/" + filename
    output_path = cwd + "/output/predict/" + filename
    yolo_process(save_path)
    pil_img = Image.open(output_path, mode='r')
    byte_arr = io.BytesIO()
    pil_img.save(byte_arr, format='PNG')
    encoded_img = encodebytes(byte_arr.getvalue()).decode('ascii')

    width, height = pil_img.size

    if width > 1000:
        width = width / 2
    if height > 1000:
        height = height /2

    response = {
        "success": True,
        "message": "predict success",
        "result": encoded_img,
        "width": width,
        "height": height
    }
    return jsonify(response), 200

@app.route("/upload", methods=["POST"])
def upload():
    if "snake_image" not in request.files:
        response = {
            "success": False,
            "message": "image not found in request"
        }
        return jsonify(response), 400

    file = request.files["snake_image"]

    if file.filename == "":
        response = {
            "success": False,
            "message": "image not found in request"
        }
        return jsonify(response), 400

    if not (file and allowed_file(file.filename)):
        response = {
            "success": False,
            "message": "invalid image extension"
        }
        return jsonify(response), 400

    filename = secure_filename(file.filename)
    cwd = os.getcwd()
    save_path = cwd + app.config['UPLOAD_FOLDER'] + "/" + filename
    file.save(save_path)

    response = {
        "success": True,
        "message": "save file success"
    }
    return jsonify(response), 200


if __name__ == "__main__":
    app.run(port=9985)