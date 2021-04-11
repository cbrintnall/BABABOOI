
import torch
import torch.nn as nn
import torchvision.models as models

from data import QuickDrawDataset
import pytorch_lightning as pl
from torch.utils.data import DataLoader


class QuickDraw(pl.LightningModule):
    def __init__(self):
        super().__init__()
        self.encoder = models.resnet18()

        self.encoder.conv1 = nn.Conv2d(1, 64, kernel_size=7, stride=2, padding=3, bias=False)
        self.encoder.fc = nn.Linear(512, 345, bias=True)

        self.loss_func = nn.CrossEntropyLoss()

    def forward(self, x):
        return self.encoder(x)

    def training_step(self, batch, batch_idx):
        x, y = batch
        pred = self.encoder(x)
        loss = self.loss_func(pred, y)

        num_correct = (pred.max(dim=1)[1] == y).float().sum()
        acc = num_correct / y.shape[0]

        self.log('train_loss', loss)
        self.log('train_acc', acc)

        return loss

    def validation_step(self, batch, batch_idx):
        x, y, = batch
        pred = self.encoder(x)
        loss = self.loss_func(pred, y)

        num_correct = (pred.max(dim=1)[1] == y).float().sum()
        num_seen = pred.shape[0]

        return {
            'loss': loss.item(),
            'num_correct': num_correct.item(),
            'num_seen': num_seen
        }

    def validation_epoch_end(self, validation_step_outputs):
        result = {
            'loss': 0,
            'num_correct': 0,
            'num_seen': 0
        }

        for part in validation_step_outputs:
            result['loss'] += part['loss']
            result['num_correct'] += part['num_correct']
            result['num_seen'] += part['num_seen']

        result['loss'] /= len(validation_step_outputs)
        acc = result['num_correct'] / result['num_seen']

        self.log('val_loss', result['loss'])
        self.log('val_acc', acc)

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=1e-3)

    def train_dataloader(self):
        train_dataset = QuickDrawDataset('splits/train.pkl', use_tmp=True)
        train_loader = DataLoader(train_dataset, batch_size=32, num_workers=4, shuffle=True)

        return train_loader

    def val_dataloader(self):
        val_dataset = QuickDrawDataset('splits/val.pkl', use_tmp=True)
        val_loader = DataLoader(val_dataset, batch_size=50, num_workers=4, shuffle=False)

        return val_loader


def main():
    model = QuickDraw()
    logger = pl.loggers.WandbLogger(project='quickdraw', entity='ayalaa2')
    trainer = pl.Trainer(
        logger=logger, gpus=4, num_nodes=1, accelerator='ddp',
        max_steps=None, precision=16, val_check_interval=2500
    )
    trainer.fit(model)
    trainer.save_checkpoint('quickdraw_model.pt')


if __name__ == '__main__':
    main()
