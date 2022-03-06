import argparse
import torch
from torch.utils.data import DataLoader
from torchvision import transforms
from CNN import CNN
from dataset import DealDataset
import pandas as pd
import warnings
import os
import time

warnings.filterwarnings("ignore")

parser = argparse.ArgumentParser(description="Test ML")
parser.add_argument("--batchsize", type=int, default=50, help="Training batch size")
parser.add_argument("--datadir", type=str, default='./data/t10k-images-idx3-ubyte.gz', help="path to data")
parser.add_argument("--labeldir", type=str, default='./data/t10k-labels-idx1-ubyte.gz', help="path to label")
parser.add_argument('--model', default='./savemodel/model_demo.pth', type=str, help='path to model')
parser.add_argument('--saveresult', default='./saveresult/result_demo.csv', type=str, help='path to save result')


def main():
    opt = parser.parse_args()
    # print(opt)

    # print("===> Loading datasets")

    test_set = DealDataset(opt.datadir, opt.labeldir, transform=transforms.ToTensor())
    test_data_loader = DataLoader(dataset=test_set, batch_size=opt.batchsize, shuffle=True)

    # print("===> Loading model")
    model = CNN()
    weights = torch.load(opt.model)
    model.load_state_dict(weights['model'].state_dict())

    # print("===> Testing")
    model.eval()
    correct_num = 0
    total_num = 0
    result = []
    for step, (x, y) in enumerate(test_data_loader):
        output = model(x)
        pred_y = torch.max(output, 1)[1]
        result.extend(pred_y.int().numpy())
        correct_num += (pred_y == y).sum().item()
        total_num += y.size(0)
    acc = correct_num / total_num
    print("Acc:{}".format(acc))

    # print("===> Saving Result")
    test = pd.DataFrame(columns=['label'], data=result)
    test.to_csv(opt.saveresult, encoding='gbk')
    # print("Result saved to {}".format(opt.saveresult))


if __name__ == "__main__":
    start_time=time.time()
    main()
    print(time.time()-start_time )