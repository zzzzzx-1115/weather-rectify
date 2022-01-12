import torch
import os
import argparse
import numpy as np
import yaml
import torch.utils.data as data
from tqdm import tqdm
from torch.utils.data.dataloader import DataLoader
from dataset import gridDataset
from confidenceTrainer import ConfidenceTrainer
from combinatorialTrainer import CombinatorialTrainer

parser = argparse.ArgumentParser()
parser.add_argument("--model", type=str, default="confidence")
parser.add_argument("--modelname", type=str, default="confidence")
parser.add_argument(
    "--test",
    type=bool,
    default=False,
)
parser.add_argument(
    "--checkpoint_path",
    type=str,
    default='checkpoint/confidence.pth',
)
opts = parser.parse_args()


def main():
    config = yaml.load(open('config.yaml', 'r'), Loader=yaml.FullLoader)

    device = 'cuda'
    epoch = config['epoch']

    train_dataset = gridDataset(config['train_dir'], isTrain=True)
    evaluate_dataset = gridDataset(config['train_dir'], isTrain=False)
    train_iter = DataLoader(train_dataset,
                            batch_size=config['batch_size'],
                            num_workers=config['num_workers'],
                            shuffle=True,
                            pin_memory=True)
    evaluate_iter = DataLoader(evaluate_dataset,
                               batch_size=1,
                               shuffle=False,
                               pin_memory=True)

    if opts.test:

        if opts.model == 'confidence':
            trainer = ConfidenceTrainer(train_iter, evaluate_iter, device,
                                        opts.modelname).to(device)
            trainer.initialize(opts.checkpoint_path)
            trainer.confidence_evaluate()
        elif opts.model == 'combinatorial':
            trainer = CombinatorialTrainer(config['combinatotorial'],
                                           train_iter, evaluate_iter, device,
                                           opts.modelname).to(device)
        else:
            print('There is no correlated model!')
    else:

        if opts.model == 'confidence':
            trainer = ConfidenceTrainer(train_iter, evaluate_iter, device,
                                        opts.modelname).to(device)
            trainer.confidence_train(epoch=1000,
                                     lr=0.0001,
                                     save_path='checkpoint/confidence1.pth')
        elif opts.model == 'combinatorial':
            trainer = CombinatorialTrainer(config['combinatotorial'],
                                           train_iter, evaluate_iter, device,
                                           opts.modelname).to(device)
            trainer.encoder_train(epoch=1000,
                                  lr=0.1,
                                  save_path1='checkpoint/encoder3.pth',
                                  save_path2='checkpoint/decoder3.pth')
        else:
            print('There is no correlated model!')
        #trainer.confidence_train()


if __name__ == "__main__":
    main()