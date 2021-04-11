import base64
import io
import os
from PIL import Image

from flask import Flask, jsonify, request
import numpy as np
import onnxruntime
from transformers import pipeline


app = Flask(__name__)
qd_mdl = os.environ.get("QUICKDRAW_MDL")
nf_mdl = os.environ.get("NLPFEUD_MDL")

ort_session_qd = onnxruntime.InferenceSession(qd_mdl)
unmasker_nf = pipeline('fill-mask', model=nf_mdl)

def img_from_b64(img_b64):
    # Convert b64 encoded bytes image to numpy
    img_bytes = base64.b64decode(img_b64)
    img = Image.open(io.BytesIO(img_bytes))
    img = np.expand_dims(np.array(img), axis=0)
    return img.astype(np.float32)


def get_prediction(images):
    # Run image through network
    ort_inputs = {ort_session_qd.get_inputs()[0].name: np.stack(images)}
    ort_outs = ort_session_qd.run(None, ort_inputs)[0]

    # Postprocess logits into class probabilities
    exp = np.exp(ort_outs)
    probs = exp / np.expand_dims(np.sum(exp, axis=1), axis=1)
    return probs


@app.route('/quickdraw', methods=['POST'])
def predict_qd():
    if request.method == 'POST':
        images = [img_from_b64(img_64) for img_64 in request.json]
        probs = get_prediction(images)
        return jsonify({'probs': probs.tolist()})


@app.route('/nlpfeud', methods=['POST'])
def predict_nf():
    if request.method == 'POST':
        probs = unmasker_nf(request.json)
        for i, dct in enumerate(probs):
            probs[i] = [dct['token_str'], dct['score']]
        return jsonify({'probs': probs})


if __name__ == '__main__':
    app.run()
