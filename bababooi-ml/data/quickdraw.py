
import pickle
import random
import json
import torch
import tqdm

from skimage.draw import line
from torch.utils.data import Dataset


class QuickDrawDataset(Dataset):

    def __init__(self, split_path, use_tmp=False):
        self.samples = pickle.load(open(split_path, 'rb'))
        self.data = {}
        self.keys = []

        for class_name in tqdm.tqdm(self.samples, desc='Loading data'):
            file_path = f'/tmp/raw_data/{class_name}.ndjson' if use_tmp else f'raw_data/{class_name}.ndjson'

            with open(file_path) as class_file:
                self.data[class_name] = []
                all_lines = class_file.readlines()

                for i, line_index in enumerate(self.samples[class_name]):
                    self.data[class_name].append(all_lines[line_index])         
                    self.keys.append((class_name, i))           

        self.class_names = sorted(list(self.data.keys()))

    def __len__(self):
        return len(self.keys)

    def create_image(self, strokes):
        img = torch.zeros((256, 256))

        for y_stroke, x_stroke in strokes:
            for i in range(len(x_stroke) - 1):
                x0 = x_stroke[i]
                x1 = x_stroke[i + 1]
                y0 = y_stroke[i]
                y1 = y_stroke[i + 1]

                rr, cc = line(x0, y0, x1, y1)
                img[rr, cc] = 1.0

        return img.unsqueeze(0)

    def __getitem__(self, k):
        class_name, line_index = self.keys[k]
        strokes = json.loads(self.data[class_name][line_index])['drawing']
        img = self.create_image(strokes)

        return img, self.class_names.index(class_name)
