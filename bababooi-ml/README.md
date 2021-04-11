# Inference Model Serving

Run the following to start serving the models via Flask. The only serving requirements are *flask*, *numpy*, *transformers*, and *onnxruntime*.
```shell
FLASK_APP=serve.py MODEL=[path-to-onnx-file] flask run
```

## API

| Method      | URL         | Json                              | Returns                           |
| ----------- | ----------- | --------------------------------- | --------------------------------- |
| POST        | /quickdraw  | List of base64 encoded images     | List of probability distributions |
| POST        | /nlpfeud    | String containing a [mask] symbol | Top five word and probabilities   |

## Minimal Python Example

```python
import base64
import requests
from PIL import Image
import io

# Quickdraw Images
images = [Image.new('L', (256, 256)) for _ in range(4)]
for i, image in enumerate(images):
    image_bytes = io.BytesIO()
    image.save(image_bytes, 'png')
    images[i] = base64.b64encode(image_bytes.getvalue()).decode('ascii')

response = requests.post('http://127.0.0.1:5000/quickdraw', json=images)
print(response.json())

# NLP Feud Text
text = 'I love driving my [MASK] to work!'
json = requests.post('http://127.0.0.1:5000/nlpfeud', json=text)
print(response.json())
```
