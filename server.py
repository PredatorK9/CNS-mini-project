import os
import numpy as np
from PIL import Image
from flask import Flask
from flask import render_template
from flask import request
import stega


app = Flask(__name__)
UPLOAD_FOLDER = './static'
RESULT_FOLDER = './results'


@app.route("/", methods=["GET", "POST"])
def main_page():
    return render_template("index.html")


@app.route("/encryption", methods=["GET", "POST"])
def encode_page():
    if request.method == 'POST':
        decoy_image_file = request.files["decoy_image"]
        hide_image_file = request.files["hide_image"]
        if decoy_image_file and hide_image_file:
            decoy_image_file.save(os.path.join(UPLOAD_FOLDER, decoy_image_file.filename))
            hide_image_file.save(os.path.join(UPLOAD_FOLDER, hide_image_file.filename))

            image_to_hide_path = os.path.join(UPLOAD_FOLDER, hide_image_file.filename)
            image_to_hide_in_path = os.path.join(UPLOAD_FOLDER, decoy_image_file.filename)

            image_to_hide = np.array(Image.open(image_to_hide_path))
            image_to_hide_in = np.array(Image.open(image_to_hide_in_path))

            encoded_image = stega.encode(image_to_hide, image_to_hide_in, 2)

            encoded_image.save(os.path.join(RESULT_FOLDER, "encoded_image.png"))

            os.remove(os.path.join(UPLOAD_FOLDER, decoy_image_file.filename))
            os.remove(os.path.join(UPLOAD_FOLDER, hide_image_file.filename))
            return render_template("success.html")

    return render_template("encode.html")


@app.route("/decryption", methods=["GET", "POST"])
def decode_page():
    if request.method == 'POST':
        encoded_image_file = request.files["encoded_image"]
        if encoded_image_file:
            encoded_image_file.save(os.path.join(UPLOAD_FOLDER, encoded_image_file.filename))

            encoded_image_path = os.path.join(UPLOAD_FOLDER, encoded_image_file.filename)
            encoded_image = np.array(Image.open(encoded_image_path))

            decoded_image = stega.decode(encoded_image, 2)
            #TODO: Change the path of the saved images
            decoded_image.save(os.path.join(RESULT_FOLDER, "decoded_image.png"))
            os.remove(os.path.join(UPLOAD_FOLDER, encoded_image_file.filename))
            return render_template("success.html")

    return render_template("decode.html")


if __name__ == "__main__":
    app.run(port=12000, debug=True)