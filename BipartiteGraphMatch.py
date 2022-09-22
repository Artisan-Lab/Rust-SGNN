from flowChart import *
import time
from MyDataset import MyOwnDataset, CodePairs, CodePairsTest, sample_path, test_path, Result, CodePair

import os


path1 = r".\test_dataset\boxed\raw"


class Edge(object):
    def __init__(self, index1, index2, weight):
        self.f = index1
        self.t = index2
        self.w = weight


class DataPair(object):
    def __init__(self, g1, g2, sim):
        self.g1 = g1
        self.g2 = g2
        self.sim = sim

    def cal_bit_sim(self):
        edges = []
        for i in range(len(self.g1)):
            for j in range(len(self.g2)):
                f = self.g1[i]
                t = self.g2[j]
                w = self.minDistance(f.label, t.label)
                edges.append(Edge(i, j, w))

        pass

    def minDistance(self, word1: str, word2: str) -> int:
        n = len(word1)
        m = len(word2)

        if n * m == 0:
            return n + m

        D = [[0] * (m + 1) for _ in range(n + 1)]


        for i in range(n + 1):
            D[i][0] = i
        for j in range(m + 1):
            D[0][j] = j


        for i in range(1, n + 1):
            for j in range(1, m + 1):
                left = D[i - 1][j] + 1
                down = D[i][j - 1] + 1
                left_down = D[i - 1][j - 1]
                if word1[i - 1] != word2[j - 1]:
                    left_down += 1
                D[i][j] = min(left, down, left_down)

        return D[n][m]


def minDistance(word1: str, word2: str) -> int:
    n = len(word1)
    m = len(word2)


    if n * m == 0:
        return n + m


    D = [[0] * (m + 1) for _ in range(n + 1)]


    for i in range(n + 1):
        D[i][0] = i
    for j in range(m + 1):
        D[0][j] = j


    for i in range(1, n + 1):
        for j in range(1, m + 1):
            left = D[i - 1][j] + 1
            down = D[i][j - 1] + 1
            left_down = D[i - 1][j - 1]
            if word1[i - 1] != word2[j - 1]:
                left_down += 1
            D[i][j] = min(left, down, left_down)

    return D[n][m]


def readfiles(path):

    file_list = os.listdir(path)

    result = []
    dataPairs = []
    for file in file_list:

        r1 = os.path.join(path, file)

        g1 = gen_nodes_from_rs(r1)
        result.append(g1)
    for i in range(len(result)):
        for j in range(len(result)):
            g1 = result[i]
            g2 = result[j]
            if i == j:
                dataPairs.append(DataPair(g1, g2, 1))
            else:
                dataPairs.append(DataPair(g1, g2, -1))
    return dataPairs


def sim(node1, node2):


    minWeight = 0
    for n1 in node1:
        l1 = ""
        if n1.kind ==NodeKind.ENTRY :
            l1 = "entry"
        elif n1.kind ==NodeKind.EXIT :
            l1 = "exit"
        elif n1.kind ==NodeKind.DUMMY :
            l1 = "dummy"
        else:
            l1 = n1.label

        minDis = 10000000
        for n2 in node2:
            l2 = ""
            if n2.kind == NodeKind.ENTRY:
                l2 = "entry"
            elif n2.kind == NodeKind.EXIT:
                l2 = "exit"
            elif n2.kind == NodeKind.DUMMY:
                l2 = "dummy"
            else:
                l2 = n2.label
            # n1.show()
            # n2.show()
            dis = minDistance(l1, l2)
            if dis < minDis:
                minDis = dis
        minWeight = minWeight + minDis
    return minWeight


def init():
    knowledge_code_pair: CodePairs = torch.load(sample_path)
    test_set: CodePairsTest = torch.load(test_path)
    # print("knowledge_code_pair.pair_list len is ",len(knowledge_code_pair.pair_list))
    # knowledge_code_pair.show()
    # test_set.show()

    count_test = 0
    right = 0
    API_list = knowledge_code_pair.api_name_kind_list;
    all_result = []
    for idx in range(len(test_set.pair_list)):
        cp1 = test_set.pair_list[idx]
        # cp1.show()
        code1 = cp1.unsafe_code
        nodelist1 = gen_nodes_from_rs(code1)

        # candidate = knowledge_code_pair.get_list_by_api(cp1.api_name)
        candidate = knowledge_code_pair.pair_list
        cos_candidate = []
        for j in range(len(candidate)):
            cp2 = knowledge_code_pair.pair_list[j]
            code2 = cp2.unsafe_code
            nodelist2 = gen_nodes_from_rs(code2)
            sim12 = sim(nodelist1, nodelist2)

            # g1 = GNN1(x1, u1, edge1)
            # g2 = GNN2(x2, u2, edge2)
            cos_candidate.append(sim12)
        max_cos = 10000000
        max_index = -1
        for j in range(len(cos_candidate)):
            value = cos_candidate[j]
            if value < max_cos:
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

def init_by_scale(scale):
    knowledge_code_pair: CodePairs = torch.load(sample_path)
    test_set: CodePairsTest = torch.load(test_path)
    # knowledge_code_pair.show()
    # test_set.show()
    # test_set = test_set[0:scale]

    count_test = 0
    right = 0
    API_list = knowledge_code_pair.api_name_kind_list;
    all_result = []
    time_start = time.time()
    for idx in range(len(test_set.pair_list)):
        cp1 = test_set.pair_list[idx]
        # cp1.show()
        code1 = cp1.unsafe_code
        nodelist1 = gen_nodes_from_rs(code1)

        # candidate = knowledge_code_pair.get_list_by_api(cp1.api_name)
        candidate = knowledge_code_pair.pair_list[0:scale]
        cos_candidate = []
        for j in range(len(candidate)):
            cp2 = knowledge_code_pair.pair_list[j]
            code2 = cp2.unsafe_code
            nodelist2 = gen_nodes_from_rs(code2)
            sim12 = sim(nodelist1, nodelist2)

            # g1 = GNN1(x1, u1, edge1)
            # g2 = GNN2(x2, u2, edge2)
            cos_candidate.append(sim12)
        max_cos = 10000000
        max_index = -1
        for j in range(len(cos_candidate)):
            value = cos_candidate[j]
            if value < max_cos:
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
    time_end = time.time()
    time_cost = time_end - time_start
    # print("------------------------------")
    # print("right is: ", right)
    # print("count is: ", count_test)
    # print("rate is: ", right / count_test)
    # print("------------------------------")

    return time_cost

if __name__ == '__main__':
    # root = r"G:\Asset\Programs\Python3\NNDL\HW1\Rust-unsafe-to-safe-code-retrivial\test_dataset\boxed"
    # orgin_path = r"G:\Asset\Programs\Python3\NNDL\HW1\Rust-unsafe-to-safe-code-retrivial\test_dataset\boxed\raw"

    # dataset = MyOwnDataset(root)
    # g1,g2,s,t1,t2 = dataset[0]
    # print(t1)
    # print(t2)
    # print(s)

    init()

    # time_start = time.time()
    # count = 0
    # for i in range(100000):
    #     count = count+1
    # time_end = time.time()
    # print('time cost', time_end - time_start, 's')
