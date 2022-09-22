import torch
from torch import nn
from torch.nn import Sequential, Linear, ReLU, Tanh,functional
from torch_geometric.nn import MessagePassing
from torch.utils.data import Dataset, DataLoader
from torch.utils.data.dataset import T_co
import pandas
import numpy
from MyDataset import MyOwnDataset, CodePairs, CodePairsTest, sample_path, test_path, Result, CodePair

from flowChart import *



inchannel = 5
embedding_size = 4  # outchannel
T = 4
learning_rate = 0.05
epoch = 100


class ACFGConv(MessagePassing):
    def __init__(self, in_channels, out_channels):

        super().__init__(aggr="add")  # "Add" aggregation (Step 5).
        self.w1 = torch.nn.Linear(in_channels, out_channels)
        self.sigmod = Sequential(
            Linear(out_channels, out_channels),
            ReLU(),
            Linear(out_channels, out_channels),
            ReLU(),
            Linear(out_channels, out_channels),
            Tanh()
        )

    def forward(self, x, u, edge_index):
        # print("----in forward----")
        #
        # print(edge_index)
        # print("x is ", x)
        # print("u is ", u)
        self.x = x

        out = self.propagate(edge_index, x=x, u=u)
        # print("out is ", out)
        return out

    def message(self, u_j):
        # print("----in message----")
        # # x_j has shape [E, out_channels]
        # print("u_j is ", u_j)

        return u_j

    def update(self, inputs):
        x = self.w1(self.x)
        sigmod_all_u = self.sigmod(inputs)
        # print("inputs is", inputs)
        # print("w1x is ", x)
        # print("sigmod_all_u is ", sigmod_all_u)

        # result = ReLU(x + sigmod_all_u)
        result = x + sigmod_all_u
        result = torch.nn.functional.relu(result)

        return result


class SiameseNetwork(nn.Module):
    def __init__(self, in_channels, out_channels):
        super(SiameseNetwork, self).__init__()
        self.w2 = Linear(out_channels, out_channels)
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.conv = []
        for t in range(T):
            self.conv.append(ACFGConv(in_channels, out_channels))

    def forword_once(self, x, u, edge_index):

        for t in range(T):
            u = self.conv[t](x, u, edge_index)

        e = torch.zeros([1, u.shape[0]])
        e = e + 1
        g = torch.matmul(e, u)
        g = self.w2(g)
        return g

    def forward(self, x1, u1, edge_index1, x2, u2, edge_index2):
        input1 = self.forword_once(x1, u1, edge_index1)
        input2 = self.forword_once(x2, u2, edge_index2)

        return input1, input2


class SiameseNetworkRespective(nn.Module):
    def __init__(self, in_channels, out_channels):
        super(SiameseNetworkRespective, self).__init__()
        self.w2 = Linear(out_channels, out_channels)
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.conv = ACFGConv(in_channels, out_channels)

    def forward(self, x, u, edge_index):

        for t in range(T):
            u = self.conv(x, u, edge_index)

        # print("u is ", u)
        e = torch.zeros([1, u.shape[0]])
        e = e + 1
        g = torch.matmul(e, u)
        g = self.w2(g)
        return g




def train():

    root = ".\\database"
    # 训练集
    dataset = MyOwnDataset(root)
    # mid = int(len(dataset) * 2 / 3)
    # mid = 4000
    # dataset_train = dataset[0:mid]
    dataset_train = dataset

    # 测试集
    # dataset_val = dataset[mid:len(dataset)]
    knowledge_code_pair = torch.load(sample_path)

    # print(type(knowledge_code_pair))
    # knowledge_code_pair.pair_list[0].show()
    # knowledge_code_pair.show()

    test_set: CodePairsTest = torch.load(test_path)
    # print(type(test_set))
    # test_set.pair_list[0].show()

    loss = nn.CosineEmbeddingLoss(margin=0.5)
    GNN1 = SiameseNetworkRespective(in_channels=inchannel, out_channels=embedding_size)
    GNN2 = SiameseNetworkRespective(in_channels=inchannel, out_channels=embedding_size)
    optim1 = torch.optim.Adam(GNN1.parameters(), lr=learning_rate)
    optim2 = torch.optim.Adam(GNN2.parameters(), lr=learning_rate)
    cos = torch.nn.CosineSimilarity()

    GNN1.train()
    GNN2.train()
    for i in range(epoch):
        print(f"epoch:{i}")
        running_loss = 0.0
        count = 0
        recall = 0
        accuracy = 0
        precision = 0
        TP = 0
        TN = 0
        FP = 0
        FN = 0
        F1_max = 0
        for data in dataset_train:
            data1, data2, simlarity, t1, t2, l1, n1, l2, n2 = data
            # print(g1, g2, simlarity)
            if simlarity == 1:
                similarity_g1_g2 = torch.tensor([1])
            else:
                similarity_g1_g2 = torch.tensor([-1])
            x1 = data1.x
            edge_index1 = data1.edge_index
            x2 = data2.x
            edge_index2 = data2.edge_index

            u1 = torch.zeros(x1.shape[0], embedding_size)
            u2 = torch.zeros(x2.shape[0], embedding_size)
            # print(f"x1 is {x1}, x2 is{x2},e1 is{edge_index1},e2 is{edge_index2}")
            # print(f"u is{u}")
            g1 = GNN1(x1, u1, edge_index1)
            g2 = GNN2(x2, u2, edge_index2)

            result_loss = loss(g1, g2, similarity_g1_g2)
            optim1.zero_grad()
            optim2.zero_grad()
            result_loss.backward()
            optim1.step()
            optim2.step()

            if (similarity_g1_g2 > 0.5):
                # print(f"simlarity is {similarity_g1_g2},cos is {cos(g1, g2)}")
                recall = recall + 1
                if (cos(g1, g2) > 0.5):
                    TP = TP + 1
                else:
                    FN = FN + 1
            else:
                if (cos(g1, g2) > 0.5):
                    FP = FP + 1
                else:
                    TN = TN + 1

            # print(f"g1 is {g1},g2 is{g2},loss is {result_loss}")

            running_loss = running_loss + result_loss
            count = count + 1

        if TP + FN == 0:
            TP = TP + 1
        precision = TP / (TP + FP)
        recall = TP / (TP + FN)
        F1 = 2 * precision * recall / (precision + recall)
        if F1 > F1_max:
            F1_max = F1
        print("F1 score", F1)
        print("F1 max score", F1_max)
        print("recall", TP / (TP + FN))
        print("precision", TP / (TP + FP))
        print("accuracy", (TP + TN) / (TP + TN + FP + FN))


        # total_test_loss = 0.0
        # count_test = 0
        # recall = 0
        # accuracy = 0
        # precision = 0
        # right = 0
        # TP = 0
        # TN = 0
        # FP = 0
        # FN = 0
        # F1 = 0;
        # F1_max = -1;
        # API_list = knowledge_code_pair.api_name_kind_list;
        # all_result = []
        # for idx in range(len(test_set.pair_list)):
        #     cp1 = test_set.pair_list[idx]
        #     # cp1.show()
        #     acfg1 = cp1.acfg
        #     x1 = acfg1.x
        #     edge1 = acfg1.edge_index
        #     u1 = torch.zeros(x1.shape[0], embedding_size)
        #     candidate = knowledge_code_pair.get_list_by_api(cp1.api_name)
        #     cos_candidate = []
        #     for j in range(len(candidate)):
        #         cp2 = candidate[j]
        #         acfg2 = cp2.acfg
        #         x2 = acfg2.x
        #         edge2 = acfg2.edge_index
        #         u2 = torch.zeros(x2.shape[0], embedding_size)
        #         g1 = GNN1(x1, u1, edge1)
        #         g2 = GNN2(x2, u2, edge2)
        #         cos_candidate.append(cos(g1, g2))
        #     max_cos = -2
        #     max_index = -1
        #     for j in range(len(cos_candidate)):
        #         value = cos_candidate[j]
        #         if value > max_cos:
        #             max_cos = value
        #             max_index = j
        #     match_result = Result(cp1, candidate[max_index], max_cos)
        #     # print(f"github code label is {cp1.api_label}")
        #     # print(f"recommendation code label is {candidate[max_index].api_label}")
        #     all_result.append(match_result)
        #
        # conunt_result = 0
        # for result in all_result:
        #     count_test = count_test + 1
        #     # print(f"-----------{conunt_result}----------------")
        #     # print(f"github code label is {result.cp1.api_label}")
        #     all_label: str = result.cp1.api_label
        #     temp = all_label.rsplit("-")
        #     # print(f"temp is {temp}")
        #     ans_list = []
        #     ans_list.append(temp[0])
        #     if len(temp) == 1:
        #         pass
        #     else:
        #         name_list = temp[0].rsplit("_", 1)
        #         name = name_list[0]
        #         for k in range(1, len(temp)):
        #             ans_list.append(name + "_" + temp[k])
        #     # print("ans_list is", ans_list)
        #     if result.cp2.api_label in ans_list:
        #         right = right + 1
        #
        #     # print(f"recommendation code label is {result.cp2.api_label}")
        #     # result.cp1.show()
        #     # result.cp2.show()
        #     # print(f"sim is {result.cos_sim}")
        #     conunt_result = conunt_result + 1
        # print("------------------------------")
        # print("right is: ", right)
        # print("count is: ", count_test)
        # print("rate is: ", right / count_test)
        # print("------------------------------")
        torch.save(GNN1, f".\\model\\model2Save\\GNN1_{i}.pth")
        torch.save(GNN2, f".\\model\\model2Save\\GNN2_{i}.pth")

    return


if __name__ == '__main__':
    train()

