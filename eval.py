import torch

from flowChart import *
import time
from MyDataset import MyOwnDataset, CodePairs, CodePairsTest, sample_path, test_path, Result, CodePair

import os
import matplotlib.pyplot as plt
import BipartiteGraphMatch
from BipartiteGraphMatch import init_by_scale
from SGNN import *

embedding_size = 4


def perform_GNN(gnn1, gnn2, scale):
    cos = torch.nn.CosineSimilarity()
    knowledge_code_pair: CodePairs = torch.load(sample_path)
    test_set: CodePairsTest = torch.load(test_path)
    count_test = 0
    right = 0
    API_list = knowledge_code_pair.api_name_kind_list
    all_result = []
    time_start = time.time()
    for idx in range(len(test_set.pair_list)):
        cp1 = test_set.pair_list[idx]
        # cp1.show()
        acfg1 = cp1.acfg
        x1 = acfg1.x
        edge1 = acfg1.edge_index
        u1 = torch.zeros(x1.shape[0], embedding_size)
        candidate = knowledge_code_pair.pair_list[0:scale]
        cos_candidate = []
        for j in range(len(candidate)):
            cp2 = candidate[j]
            acfg2 = cp2.acfg
            x2 = acfg2.x
            edge2 = acfg2.edge_index
            u2 = torch.zeros(x2.shape[0], embedding_size)
            g1 = gnn1(x1, u1, edge1)
            g2 = gnn2(x2, u2, edge2)
            cos_candidate.append(cos(g1, g2))
        max_cos = -2
        max_index = -1
        for j in range(len(cos_candidate)):
            value = cos_candidate[j]
            if value > max_cos:
                max_cos = value
                max_index = j
        match_result = Result(cp1, candidate[max_index], max_cos)
        # print(f"github code label is {cp1.api_label}")
        # print(f"recommendation code label is {candidate[max_index].api_label}")
        all_result.append(match_result)

    conunt_result = 0
    for result in all_result:
        count_test = count_test + 1
        # print(f"-----------{conunt_result}----------------")
        # print(f"github code label is {result.cp1.api_label}")
        all_label: str = result.cp1.api_label
        temp = all_label.rsplit("-")
        # print(f"temp is {temp}")
        ans_list = []
        ans_list.append(temp[0])
        if len(temp) == 1:
            pass
        else:
            name_list = temp[0].rsplit("_", 1)
            name = name_list[0]
            for k in range(1, len(temp)):
                ans_list.append(name + "_" + temp[k])
        # print("ans_list is", ans_list)
        if result.cp2.api_label in ans_list:
            right = right + 1

        # print(f"recommendation code label is {result.cp2.api_label}")
        # result.cp1.show()
        # result.cp2.show()
        # print(f"sim is {result.cos_sim}")
        conunt_result = conunt_result + 1
    # print("------------------------------")
    # print("right is: ", right)
    # print("count is: ", count_test)
    # print("rate is: ", right / count_test)
    # print("------------------------------")
    time_end = time.time()
    time_cost = time_end - time_start
    return time_cost

def perform_GNN_right_rate(GNN1, GNN2):
    cos = torch.nn.CosineSimilarity()
    test_set: CodePairsTest = torch.load(test_path)
    knowledge_code_pair = torch.load(sample_path)
    count_test = 0
    right = 0
    API_list = knowledge_code_pair.api_name_kind_list
    all_result = []
    for idx in range(len(test_set.pair_list)):
        cp1 = test_set.pair_list[idx]
        # cp1.show()
        acfg1 = cp1.acfg
        x1 = acfg1.x
        edge1 = acfg1.edge_index
        u1 = torch.zeros(x1.shape[0], embedding_size)
        candidate = knowledge_code_pair.get_list_by_api(cp1.api_name)
        cos_candidate = []
        for j in range(len(candidate)):
            cp2 = candidate[j]
            acfg2 = cp2.acfg
            x2 = acfg2.x
            edge2 = acfg2.edge_index
            u2 = torch.zeros(x2.shape[0], embedding_size)
            g1 = GNN1(x1, u1, edge1)
            g2 = GNN2(x2, u2, edge2)
            cos_candidate.append(cos(g1, g2))
        max_cos = -2
        max_index = -1
        for j in range(len(cos_candidate)):
            value = cos_candidate[j]
            if value > max_cos:
                max_cos = value
                max_index = j
        match_result = Result(cp1, candidate[max_index], max_cos)
        # print(f"github code label is {cp1.api_label}")
        # print(f"recommendation code label is {candidate[max_index].api_label}")
        all_result.append(match_result)

    conunt_result = 0
    for result in all_result:
        count_test = count_test + 1
        # print(f"-----------{conunt_result}----------------")
        # print(f"github code label is {result.cp1.api_label}")
        all_label: str = result.cp1.api_label
        temp = all_label.rsplit("-")
        # print(f"temp is {temp}")
        ans_list = []
        ans_list.append(temp[0])
        if len(temp) == 1:
            pass
        else:
            name_list = temp[0].rsplit("_", 1)
            name = name_list[0]
            for k in range(1, len(temp)):
                ans_list.append(name + "_" + temp[k])
        # print("ans_list is", ans_list)
        if result.cp2.api_label in ans_list:
            right = right + 1

        # print(f"recommendation code label is {result.cp2.api_label}")
        # result.cp1.show()
        # result.cp2.show()
        # print(f"sim is {result.cos_sim}")
        conunt_result = conunt_result + 1
    print("------------------------------")
    print("right is: ", right)
    print("count is: ", count_test)
    print("rate is: ", right / count_test)
    print("------------------------------")
    return

def cal_right_rate():
    print("-----Code recommendation accuracy----")
    b2_model1 = torch.load(
        ".\\model\\model2Save\\GNN1_94.pth")
    b2_model2 = torch.load(
        ".\\model\\model2Save\\GNN2_94.pth")
    GNN1 = torch.load(
        ".\\model\\modelSave\\GNN1_99.pth")
    GNN2 = torch.load(
        ".\\model\\modelSave\\GNN2_99.pth")

    print("Siamese Neural Network")
    perform_GNN_right_rate(GNN1, GNN2)

    print("Neural Network-based Graph Embedding")
    perform_GNN_right_rate(b2_model1, b2_model2)

    print("Bipartite Graph Matching.")
    BipartiteGraphMatch.init()



def cal_time():
    print("----Code recommendation accuracy----")
    tlist = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 123]
    b2_model1 = torch.load(
        ".\\model\\model2Save\\GNN1_99.pth")
    b2_model2 = torch.load(
        ".\\model\\model2Save\\GNN2_99.pth")
    GNN1 = torch.load(
        ".\\model\\modelSave\\GNN1_99.pth")
    GNN2 = torch.load(
        ".\\model\\modelSave\\GNN2_99.pth")
    b1_time_list = []
    b2_time_list = []
    gnn_time_list = []



    print("Siamese Neural Network")
    for t in tlist:
        t3 = perform_GNN(GNN1, GNN2,t)
        gnn_time_list.append(t3)
        print(t3)

    print("Neural Network-based Graph Embedding")
    for t in tlist:
        t2 = perform_GNN(b2_model1, b2_model2, t)
        b2_time_list.append(t2)
        print(t2)

    print("Bipartite Graph Matching.")
    for t in tlist:
        time_b1 = init_by_scale(t)
        print("b1 time is ",time_b1," s")
        b1_time_list.append(time_b1)


if __name__ == "__main__":
    cal_right_rate()
    cal_time()
