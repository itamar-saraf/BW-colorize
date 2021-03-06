import pytorch_lightning as pl
import torch
from torch import nn


class Conv(pl.LightningModule):
    def __init__(self, input_c, output_c, kernel=3, stride=1, padding=1, bias=False):
        super().__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(input_c, output_c, (kernel, kernel), stride=(stride, stride),
                      padding=(padding, padding), bias=bias),
            nn.BatchNorm2d(output_c),
            nn.LeakyReLU(0.2),
            nn.Conv2d(output_c, output_c, (kernel, kernel), stride=(stride, stride),
                      padding=(padding, padding), bias=bias),
            nn.BatchNorm2d(output_c),
            nn.LeakyReLU(0.2),
        )

    def forward(self, x):
        x = self.conv(x)
        return x


class DeConv(pl.LightningModule):
    def __init__(self, input_c, output_c, kernel=3, stride=2, padding=1, output_padding=1):
        super().__init__()
        self.deconv = nn.ConvTranspose2d(input_c // 2, input_c // 2, (kernel, kernel),
                                         padding=(padding, padding), stride=(stride, stride),
                                         output_padding=(output_padding, output_padding))
        self.conv = Conv(input_c, output_c)

    def forward(self, x, skip_x):
        x = self.deconv(x)
        x = torch.cat((skip_x, x), axis=1)
        x = self.conv(x)
        return x
