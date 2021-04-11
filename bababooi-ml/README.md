# Inference Model Serving

Run the following to start serving the models via Flask. The only serving requirements are *flask*, *numpy*, and *onnxruntime*.
```shell
FLASK_APP=serve.py MODEL=[path-to-onnx-file] flask run
```

## API

| Method      | URL         | Json                          | Returns                           |
| ----------- | ----------- | ----------------------------- | --------------------------------- |
| POST        | /predict    | List of base64 encoded images | List of probability distributions |

## Minimal Python Example
```python
import base64
import requests
from PIL import Image
import io

images = [Image.new('L', (256, 256)) for _ in range(4)]
for i, image in enumerate(images):
    image_bytes = io.BytesIO()
    image.save(image_bytes, 'png')
    images[i] = base64.b64encode(image_bytes.getvalue()).decode('ascii')

json = requests.post('http://127.0.0.1:5000/predict', json=images)
print(json.content)
```