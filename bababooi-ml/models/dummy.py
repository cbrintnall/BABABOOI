from pytorch_lightning import LightningModule
import torch
import torch.nn as nn


class DummyModel(LightningModule):
    def __init__(self, channels=1, classes=10):
        """Dummy model for testing ONNX exports and serving.

        Args:
            channels (int): Number of channels in input image. Defaults to 1 for grayscale.
            classes (int): Number of classes for multi-class classification. Defaults to 10.
        """
        super().__init__()
        self.save_hyperparameters()

        self.conv = nn.Conv2d(channels, 8, 3)
        self.pool = nn.AdaptiveAvgPool2d(2)
        self.proj = nn.Linear(8*2*2, classes)

    def forward(self, x):
        x = self.conv(x)
        x = self.pool(x)
        x = x.flatten(1)
        x = self.proj(x)
        return x

    def _step(self, img, targ):
        pred = self(img)
        return nn.functional.cross_entropy(pred, targ)

    def training_step(self, batch, batch_idx):
        return self._step(*batch)

    def validation_step(self, batch, batch_idx):
        return self._step(*batch)

    def test_step(self, batch, batch_idx):
        return self._step(*batch)

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=1e-3)


def main():
    model = DummyModel()

    # (batch x channels x height x width) data sample.
    # (batch x classes) prediction.
    x = torch.randn(1, 1, 256, 256, dtype=torch.float)
    y = model(x)
    assert y.shape == (1, 10)
    print(f'Transformed {x.shape} to {y.shape}.')


if __name__ == "__main__":
    main()
