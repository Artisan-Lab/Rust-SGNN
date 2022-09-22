import SGNN,Gmini
import torch
from torch import nn
from torch.nn import Sequential, Linear, ReLU, Tanh
from torch_geometric.nn import MessagePassing
from torch.utils.data import Dataset, DataLoader
from torch.utils.data.dataset import T_co
import pandas
import numpy
from MyDataset import MyOwnDataset, CodePairs, CodePairsTest, sample_path, test_path, Result, CodePair
from flowChart import *

if __name__ == '__main__':
    print("----train SGNN----")
    SGNN.train()
    print("----train Gmini----")
    Gmini.train()