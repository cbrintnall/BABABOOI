
import os
import json
import random
import pickle
import tqdm

train_split = {}
val_split = {}
test_split = {}

splits = (0.9, 0.025, 0.025)
MAX_SAMPLES = 50000

for file_name in tqdm.tqdm(os.listdir('raw_data')):
    class_name = file_name.split('.ndjson')[0]

    with open(os.path.join('raw_data', file_name)) as data:
        # Load the ndjson file and only keep drawings that were recognized
        dict_lines = [(line_index, line) for line_index, line in enumerate(data.readlines())]
        dict_lines = list(filter(lambda x : '"recognized":true' in x[1], dict_lines))

        # Get those line indices and shuffle them up
        valid_lines = [x[0] for x in dict_lines]
        random.shuffle(valid_lines)

        assert len(valid_lines) > MAX_SAMPLES
        i1 = int(MAX_SAMPLES * splits[0])
        i2 = int(MAX_SAMPLES * (splits[0] + splits[1]))
        i3 = MAX_SAMPLES

        # Split those valid indices into our train and test sets
        train_samples = valid_lines[:i1]
        val_samples = valid_lines[i1:i2]
        test_samples = valid_lines[i2:i3]

        assert (len(train_samples) + len(val_samples) + len(test_samples)) == MAX_SAMPLES

        # Store the train/test set
        train_split[class_name] = train_samples
        val_split[class_name] = val_samples
        test_split[class_name] = test_samples

pickle.dump(train_split, open('splits/train.pkl', 'wb'))
pickle.dump(val_split, open('splits/val.pkl', 'wb'))
pickle.dump(test_split, open('splits/test.pkl', 'wb'))
