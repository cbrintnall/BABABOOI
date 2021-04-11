import base64
import io
import os
from PIL import Image

from flask import Flask, jsonify, request
import numpy as np
import onnxruntime


app = Flask(__name__)
model_pth = os.environ.get("MODEL")
if model_pth is None:
    raise ValueError('No model specified. Please specify the MODEL environment variable.')
ort_session = onnxruntime.InferenceSession(model_pth)


def img_from_b64(img_b64):
    # Convert b64 encoded bytes image to numpy
    img_bytes = base64.b64decode(img_b64)
    img = Image.open(io.BytesIO(img_bytes))
    img = np.expand_dims(np.array(img), axis=0)
    return img.astype(np.float32)


def get_prediction(images):
    # Run image through network
    ort_inputs = {ort_session.get_inputs()[0].name: np.stack(images)}
    ort_outs = ort_session.run(None, ort_inputs)[0]

    # Postprocess logits into class probabilities
    exp = np.exp(ort_outs)
    probs = exp / np.expand_dims(np.sum(exp, axis=1), axis=1)
    return probs


@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        images = [img_from_b64(img_64) for img_64 in request.json]
        probs = get_prediction(images)
        return jsonify({'probs': probs.tolist()})


if __name__ == '__main__':
    app.run()
