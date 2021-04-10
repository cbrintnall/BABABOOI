import io
import json

import torch
from torchvision.transforms.functional import to_tensor
from PIL import Image
from flask import Flask, jsonify, request

from models import DummyModel


app = Flask(__name__)
model = DummyModel.load_from_checkpoint('lightning_logs/version_0/checkpoints/epoch=0-step=31.ckpt')
model.eval()


def transform_image(img_bytes):
    image = Image.open(io.BytesIO(img_bytes))
    image = to_tensor(image).unsqueeze(0)
    return image


def get_prediction(img_bytes):
    img = transform_image(img_bytes)
    logits = model(img)
    probs = torch.nn.functional.softmax(logits, dim=1)
    return probs


@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        file = request.files['images']
        probs = get_prediction(file.read())
        return jsonify({'probs': probs.tolist()})


if __name__ == '__main__':
    app.run()
