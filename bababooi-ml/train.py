import pytorch_lightning as pl

from data import DummyDataModule
from models import DummyModel


def main():
    data = DummyDataModule()
    model = DummyModel()
    trainer = pl.Trainer(max_epochs=1, gpus=1)
    trainer.fit(model, data)


if __name__ == '__main__':
    main()
