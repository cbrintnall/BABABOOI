import base64
import io
import os
from PIL import Image

from flask import Flask, jsonify, request
import numpy as np
import onnxruntime
from transformers import AutoTokenizer


app = Flask(__name__)
qd_mdl = os.environ.get("QUICKDRAW_MDL")
nf_mdl = os.environ.get("NLPFEUD_MDL")
ort_session_qd = onnxruntime.InferenceSession(qd_mdl)
ort_session_nf = onnxruntime.InferenceSession(nf_mdl)
tokenizer = AutoTokenizer.from_pretrained('distilbert-base-uncased')


def softmax(arr, axis):
    exp = np.exp(arr)
    probs = exp / np.sum(exp, axis=axis, keepdims=True)
    return probs


def img_from_b64(img_b64):
    # Convert b64 encoded bytes image to numpy
    img_bytes = base64.b64decode(img_b64)
    img = Image.open(io.BytesIO(img_bytes))
    img = np.expand_dims(np.array(img), axis=0)
    img = img.astype(np.float32)
    img = img / 255.0
    print(img.max())
    return img.astype(np.float32)


def get_prediction(images):
    # Run image through network
    ort_inputs = {ort_session_qd.get_inputs()[0].name: np.stack(images)}
    ort_outs = ort_session_qd.run(None, ort_inputs)[0]

    # Postprocess logits into class probabilities
    probs = softmax(ort_outs, axis=1)
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
        # Token and predict sequence
        seq = str(request.json)
        tokens = tokenizer(seq, return_tensors='pt')
        tokens = {k: v.numpy() for k, v in tokens.items()}
        token_logits = ort_session_nf.run(None, tokens)[0]

        # Get top five predictions for masked token
        mask_token_index = np.where(tokens['input_ids'] == tokenizer.mask_token_id)[1]
        mask_token_probs = softmax(token_logits[0, mask_token_index, :], axis=1)
        top5_idx = np.flip(np.argsort(mask_token_probs, axis=1), axis=1)[0, :5]
        top5_prob = mask_token_probs[0, top5_idx]
        res = [[tokenizer.decode([token]), prob.item()] for token, prob in zip(top5_idx, top5_prob)]
        return jsonify({'probs': res})


if __name__ == '__main__':
    app.run()
