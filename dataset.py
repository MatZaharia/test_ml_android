import gzip
import os
import numpy as np
from torch.utils.data import Dataset


class DealDataset(Dataset):
    """
        读取数据、初始化数据
    """

    def __init__(self, data_name, label_name, transform=None):
        (train_set, train_labels) = load_data(data_name, label_name)
        self.train_set = train_set
        self.train_labels = train_labels
        self.transform = transform

    def __getitem__(self, index):
        img, target = self.train_set[index], int(self.train_labels[index])
        if self.transform is not None:
            img = self.transform(img)
        return img, target

    def __len__(self):
        return len(self.train_set)


def load_data(data_name, label_name):
    with gzip.open(label_name, 'rb') as lbpath:  # rb表示的是读取二进制数据
        y_train = np.frombuffer(lbpath.read(), np.uint8, offset=8)

    with gzip.open(data_name, 'rb') as imgpath:
        x_train = np.frombuffer(
            imgpath.read(), np.uint8, offset=16).reshape(len(y_train), 28, 28)
    return (x_train, y_train)
