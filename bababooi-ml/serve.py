import io
import json

import torch
from torchvision.transforms.functional import to_tensor
from PIL import Image
from flask import Flask, jsonify, request
import onnxruntime
import numpy as np

from models import DummyModel


app = Flask(__name__)
ort_session = onnxruntime.InferenceSession('onnx/model.onnx')


def img_from_bytes(img_bytes):
    image = Image.open(io.BytesIO(img_bytes))
    image = np.expand_dims(np.array(image), axis=(0, 1))
    return image.astype(np.float32)


def get_prediction(img_bytes):
    # Run image through network
    img = img_from_bytes(img_bytes)
    ort_inputs = {ort_session.get_inputs()[0].name: img}
    ort_outs = ort_session.run(None, ort_inputs)[0]

    # Postprocess logits into class probabilities
    exp = np.exp(ort_outs)
    probs = exp / np.sum(exp, axis=1)
    return probs


@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        file = request.files['images']
        probs = get_prediction(file.read())
        return jsonify({'probs': probs.tolist()})


if __name__ == '__main__':
    app.run()
