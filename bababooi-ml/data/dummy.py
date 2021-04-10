from pytorch_lightning import LightningDataModule
import torch
from torch.utils.data import Dataset, DataLoader


class DummyDataModule(LightningDataModule):
    def __init__(self, pin_memory=True, classes=10):
        super().__init__()
        self.pin_memory = pin_memory
        self.classes = classes

    def setup(self, stage=None):
        if stage == 'fit':
            self.trn_data = DummyDataset(classes=self.classes)
            self.dev_data = DummyDataset(classes=self.classes, iterations=250)
        elif stage == 'test':
            self.tst_data = DummyDataset(classes=self.classes, iterations=250)

    def train_dataloader(self):
        return DataLoader(self.trn_data, num_workers=4, batch_size=32, shuffle=True, pin_memory=self.pin_memory)

    def val_dataloader(self):
        return DataLoader(self.dev_data, num_workers=4, batch_size=32, pin_memory=self.pin_memory)

    def test_dataloader(self):
        return DataLoader(self.tst_data, num_workers=4, batch_size=32, pin_memory=self.pin_memory)


class DummyDataset(Dataset):
    def __init__(self, classes, img_shape=(1, 224, 224), iterations=1000):
        self.iterations = iterations
        self.imgs = torch.randn(iterations, *img_shape)
        self.targs = torch.randint(0, classes, (iterations,))

    def __len__(self):
        return self.iterations

    def __getitem__(self, idx):
        return self.imgs[idx], self.targs[idx]
