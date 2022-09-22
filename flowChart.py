from typing import List, Any, Dict

import torch
from torch_geometric.data import Data
from DataPreprocessing import *
from enum import Enum


class NodeKind(Enum):

    SEQUENTIAL = 0
    ENTRY = 1
    EXIT = 2
    DUMMY = 3
    MIXED = 4
    USED = 5




class Node(object):

    connectedTo: dict[Any, Any]


    def __init__(self, index: int, kind: NodeKind,content , label=None):
        self.index = index
        self.kind = kind
        self.label = label
        self.content = content
        self.connectedTo = {}
        self.connectedFrom = {}

    def show(self):
        print("index is ",self.index)
        print("kind is ",self.kind)
        print("label is ",self.label)
        print("content is ",self.content)

    def add_neighbor(self, nbr, weight):
        # nbr:Node

        self.connectedTo.update({nbr: weight})

    def add_from(self,nbr,weight):
        self.connectedFrom.update({nbr:weight})

    def __str__(self):
        return str(self.index) + '-->' + str([nbr.index for nbr in self.connectedTo])

    def get_connections(self):
        return self.connectedTo.indexs()

    def get_id(self):
        return self.index

    def get_weight(self, nbr):
        weight = self.connectedTo.get(nbr)
        if weight is not None:
            return weight
        else:
            raise KeyError("No such nbr exist!")



class EdgeKind(object):

    def __init__(self, kind: str, condition=None):
        if kind == "SEQUENTIAL":
            self.name = "SEQUENTIAL"
            self.value = None
        elif kind == "FALSE":
            self.name = "FALSE"
            self.value = None
        elif kind == "TRUE":
            self.name = "TRUE"
            self.value = None
        elif kind == "MATCH_BRANCH":
            self.name = "MATCH_BRANCH"
            self.value = condition
        else:
            print("[WARNING]:the edge_kind is illegal")
            self.name = None
            self.value = None
        return

    def __str__(self):
        return str(self.__class__.__name__) + "." + str(self.name)


class Edge(object):
    def __init__(self, f: Node, t: Node, weight: EdgeKind):
        self.f = f
        self.t = t
        self.weight = weight


class Graph(object):

    def __init__(self, content: str):
        self.nodeList = {}
        self.edgeList = {}
        self.nodeEmbedding = []
        self.nodeNum = 0
        self.edgeNum = 0
        self.content = content
        self.layer = 0

    def gen_flowchart(self):
        if self.layer == 0:
            entry = Node(self.nodeNum, NodeKind.ENTRY, "")
            self.add_node(entry)
            exit = Node(self.nodeNum, NodeKind.EXIT, "")
            self.add_node(exit)
            mixedNode = Node(self.nodeNum, NodeKind.MIXED, self.content)
            self.add_node(mixedNode)

            self.add_edge(entry,mixedNode,EdgeKind("SEQUENTIAL"))
            self.add_edge(mixedNode,exit,EdgeKind("SEQUENTIAL"))

        # self.gen_subflowgraph_from_mixed(mixedNode)
        count = 0
        continueNode = None
        breakNode = None
        while self.exist_mixed_node():
            # print(f"-----in while {count}---------")
            # self.show()

            for i in self.nodeList.keys():
                node = self.nodeList[i]
                if node.kind == NodeKind.MIXED:
                    continueNode,breakNode=self.gen_subflowgraph_from_mixed(node,continueNode,breakNode)
                    break

            count += 1
        pass


    def gen_subflowgraph_from_mixed(self,mixedNode,continueNode,breakNode):

        pre = None
        next = None
        for i in self.edgeList.keys():
            edge:Edge = self.edgeList[i]
            if edge.t == mixedNode:
                pre = edge
                # print("pre")
            if edge.f == mixedNode:
                next = edge
                # print("next")

        content = mixedNode.content
        mixedNode.kind = NodeKind.USED
        # print("-----------gen_subflowgraph_from_code---------------")

        buffer = ""
        brace = -1
        label = ""
        first = -1
        lastNode = None
        lastState = None
        markIfEdge = None

        continueNodeNew = continueNode
        breakNodeNew = breakNode


        for c in content:

            buffer = buffer + c

            have_return = buffer.find("return") > -1
            have_continue = buffer.find("continue") > -1
            have_break = buffer.find("break") > -1

            if c == ';' and brace == -1 and not have_return and not have_break and not have_continue:

                if len(buffer) == 1:

                    buffer = ""
                    continue

                buffer = self.clearbuffer(buffer)
                node = Node(self.nodeNum,NodeKind.SEQUENTIAL,None,buffer)
                self.add_node(node)

                buffer = ""

                if first == -1 and pre != None :

                    pre.t = node
                    # print(f"pre.t is {pre.t.index},pre.f is {pre.f.index}")
                    # print(f"node is {node.index}")
                    # print(f"pre.f.connectedTo is {pre.f.connectedTo.keys()}")
                    # for i in pre.f.connectedTo.keys():
                    #     print(i.index)
                    # self.modify_edge_tail(pre,node)
                    first +=1

                else:

                    self.add_edge(lastNode,node,EdgeKind("SEQUENTIAL"))

                lastNode = node
                lastState = "SEQUENTIAL"

            elif c ==";" and brace == -1 and have_return and not have_break and not have_continue:

                # print("-----------return--------------")
                buffer = self.clearbuffer(buffer)
                node = Node(self.nodeNum, NodeKind.SEQUENTIAL, None, buffer)
                self.add_node(node)

                buffer = ""

                if first == -1 and pre != None:

                    pre.t = node
                    first += 1

                else:

                    self.add_edge(lastNode, node, EdgeKind("SEQUENTIAL"))


                next.t = self.nodeList[1]

                lastNode = node
                lastState = "RETURN"

            elif c ==";" and brace == -1 and not have_return and have_break and not have_continue:

                # print("-----------return--------------")
                buffer = self.clearbuffer(buffer)
                node = Node(self.nodeNum, NodeKind.SEQUENTIAL, None, buffer)
                self.add_node(node)

                buffer = ""

                if first == -1 and pre != None:

                    pre.t = node
                    first += 1

                else:

                    self.add_edge(lastNode, node, EdgeKind("SEQUENTIAL"))

                if breakNode:
                    next.t = breakNode
                    breakNodeNew = None

                lastNode = node
                lastState = "BREAK"

            elif c ==";" and brace == -1 and not have_return and not have_break and have_continue:

                # print("-----------return--------------")
                buffer = self.clearbuffer(buffer)
                node = Node(self.nodeNum, NodeKind.SEQUENTIAL, None, buffer)
                self.add_node(node)

                buffer = ""

                if first == -1 and pre != None:

                    pre.t = node
                    first += 1

                else:

                    self.add_edge(lastNode, node, EdgeKind("SEQUENTIAL"))

                if continueNode:
                    next.t = continueNode
                    continueNodeNew = None

                lastNode = node
                lastState = "CONTINUE"

            elif c == '{' :
                if brace == -1:

                    label = buffer[0:-1]
                    buffer = ""
                    brace += 1

                else:

                    brace += 1
            elif c == '}':
                if brace == 0:


                    if label.find("if") > -1 and label.find("else")==-1:


                        # if label.find("let") > -1:
                        #     letIf = True
                        # else:
                        #     letIf = False
                        label = self.clearbuffer(label)
                        node = Node(self.nodeNum, NodeKind.SEQUENTIAL, None, label)
                        self.add_node(node)
                        if first == -1 and pre != None:
                            pre.t = node
                            # self.modify_edge_tail(pre, node)
                            first += 1
                        else:
                            self.add_edge(lastNode, node, EdgeKind("SEQUENTIAL"))

                        buffer = self.clearbuffer(buffer)
                        mixed = Node(self.nodeNum,NodeKind.MIXED,buffer[0:-1])
                        self.add_node(mixed)
                        dummy = Node(self.nodeNum,NodeKind.DUMMY,None)
                        self.add_node(dummy)
                        self.add_edge(node,mixed,EdgeKind("TRUE"))
                        markIfEdge = self.add_edge(node,dummy,EdgeKind("FALSE"))
                        self.add_edge(mixed,dummy,EdgeKind("SEQUENTIAL"))
                        lastNode = dummy

                    elif label.find("else if") > -1:

                        label = self.clearbuffer(label)
                        node = Node(self.nodeNum, NodeKind.SEQUENTIAL, None, label)
                        self.add_node(node)

                        buffer = self.clearbuffer(buffer)
                        mixed = Node(self.nodeNum, NodeKind.MIXED, buffer[0:-1])
                        self.add_node(mixed)
                        dummy = Node(self.nodeNum, NodeKind.DUMMY, None)
                        self.add_node(dummy)

                        self.add_edge(node, mixed, EdgeKind("TRUE"))

                        e = self.add_edge(node, dummy, EdgeKind("FALSE"))
                        self.add_edge(mixed, dummy, EdgeKind("SEQUENTIAL"))

                        self.add_edge(dummy,markIfEdge.t, EdgeKind("SEQUENTIAL"))
                        markIfEdge.t = node
                        markIfEdge = e

                    elif label.find("else") > -1 and label.find("if") == -1:

                        # print("---find else-----!!!!!!!!!!")
                        buffer = self.clearbuffer(buffer)
                        label = self.clearbuffer(label)
                        node = Node(self.nodeNum, NodeKind.MIXED, buffer[0:-1], label)
                        self.add_node(node)
                        self.add_edge(node,markIfEdge.t,EdgeKind("SEQUENTIAL"))
                        markIfEdge.t = node

                    elif label.find("for") > -1 or label.find("while") > -1:

                        label = self.clearbuffer(label)
                        node = Node(self.nodeNum, NodeKind.SEQUENTIAL, None, label)

                        self.add_node(node)
                        if first == -1 and pre != None:
                            pre.t = node
                            # self.modify_edge_tail(pre, node)
                            first += 1
                        else:
                            self.add_edge(lastNode, node, EdgeKind("SEQUENTIAL"))
                        buffer = self.clearbuffer(buffer)

                        mixed = Node(self.nodeNum,NodeKind.MIXED,buffer[0:-1])
                        self.add_node(mixed)
                        dummy = Node(self.nodeNum,NodeKind.DUMMY,None)
                        self.add_node(dummy)

                        self.add_edge(node,mixed,EdgeKind("TRUE"))
                        self.add_edge(mixed,node,EdgeKind("SEQUENTIAL"))

                        self.add_edge(node,dummy,EdgeKind("FALSE"))
                        lastNode = dummy
                        continueNodeNew= node
                        breakNodeNew = dummy

                    elif label.find("loop") > -1:

                        label = self.clearbuffer(label)
                        node = Node(self.nodeNum, NodeKind.SEQUENTIAL, None, label)

                        self.add_node(node)
                        if first == -1 and pre != None:
                            pre.t = node
                            # self.modify_edge_tail(pre, node)
                            first += 1
                        else:
                            self.add_edge(lastNode, node, EdgeKind("SEQUENTIAL"))
                        buffer = self.clearbuffer(buffer)

                        mixed = Node(self.nodeNum,NodeKind.MIXED,buffer[0:-1])
                        self.add_node(mixed)
                        dummy = Node(self.nodeNum,NodeKind.DUMMY,None)
                        self.add_node(dummy)

                        self.add_edge(node,mixed,EdgeKind("TRUE"))
                        self.add_edge(mixed,node,EdgeKind("SEQUENTIAL"))

                        self.add_edge(node,dummy,EdgeKind("FALSE"))
                        lastNode = dummy
                        continueNodeNew= node
                        breakNodeNew = dummy

                    elif label.find("unsafe") > -1:

                        # print("find unsafe !")
                        # print("buffer is:" + buffer)
                        # print("label is:" + label)
                        label = self.clearbuffer(label)
                        node = Node(self.nodeNum, NodeKind.SEQUENTIAL, None, label)

                        self.add_node(node)
                        if first == -1 and pre != None:
                            pre.t = node
                            # self.modify_edge_tail(pre, node)
                            first += 1
                        else:
                            self.add_edge(lastNode, node, EdgeKind("SEQUENTIAL"))
                        buffer = self.clearbuffer(buffer)

                        mixed = Node(self.nodeNum, NodeKind.MIXED, buffer[0:-1])
                        self.add_node(mixed)

                        self.add_edge(node, mixed, EdgeKind("SEQUENTIAL"))
                        lastNode = mixed

                    elif label.find("use") > -1 and label.find("unused") == -1:

                        # print("find use !")
                        # print("buffer is:" + buffer)
                        # print("label is:" + label)
                        label = self.clearbuffer(label)
                        node = Node(self.nodeNum, NodeKind.SEQUENTIAL, None, label)

                        self.add_node(node)
                        if first == -1 and pre != None:
                            pre.t = node
                            # self.modify_edge_tail(pre, node)
                            first += 1
                        else:
                            self.add_edge(lastNode, node, EdgeKind("SEQUENTIAL"))
                        buffer = self.clearbuffer(buffer)

                        mixed = Node(self.nodeNum, NodeKind.MIXED, buffer[0:-1])
                        self.add_node(mixed)

                        self.add_edge(node, mixed, EdgeKind("SEQUENTIAL"))
                        lastNode = mixed
                    elif label.find("fn") > -1 == -1:

                        # print("find fn !")
                        # print("buffer is:" + buffer)
                        # print("label is:" + label)
                        label = self.clearbuffer(label)
                        node = Node(self.nodeNum, NodeKind.SEQUENTIAL, None, label)

                        self.add_node(node)
                        if first == -1 and pre != None:
                            pre.t = node
                            # self.modify_edge_tail(pre, node)
                            first += 1
                        else:
                            self.add_edge(lastNode, node, EdgeKind("SEQUENTIAL"))
                        buffer = self.clearbuffer(buffer)

                        mixed = Node(self.nodeNum, NodeKind.MIXED, buffer[0:-1])
                        self.add_node(mixed)

                        self.add_edge(node, mixed, EdgeKind("SEQUENTIAL"))
                        lastNode = mixed

                    else:

                        buffer = self.clearbuffer(buffer)
                        label = self.clearbuffer(label)
                        # print("====buffer is ===\n",buffer[0:-1])
                        if '{' in buffer[0:-1]:
                            node = Node(self.nodeNum, NodeKind.MIXED, buffer[0:-1], label)
                            self.add_node(node)
                        else:
                            node = Node(self.nodeNum,NodeKind.SEQUENTIAL,buffer[0:-1],label)
                            self.add_node(node)

                        if first == -1 and pre != None:
                            pre.t = node
                            first += 1
                        else:
                            if lastState == "SEQUENTIAL":
                                self.add_edge(lastNode, node, EdgeKind("SEQUENTIAL"))
                            else:
                                self.add_edge(lastNode, node, EdgeKind("SEQUENTIAL"))
                            pass
                        lastNode = node

                    buffer = ""
                    label = ""
                    brace -= 1

                else:
                    brace -= 1


        buffer = self.clearbuffer(buffer)
        t = buffer.replace(" ", "")

        if t != ""and t.find("return") == -1 :

            buffer = self.clearbuffer(buffer)
            # print("buffer is:"+buffer)
            # print(f"lastnode is{lastNode}")
            # print(f"first is {first}")
            # print(f"pre is {pre}")
            node = Node(self.nodeNum, NodeKind.SEQUENTIAL, None, buffer)
            self.add_node(node)

            if first == -1 and pre != None:
                pre.t = node
                first += 1
            else:
                self.add_edge(lastNode, node, EdgeKind("SEQUENTIAL"))
            lastNode = node
        elif t != "" and t.find("return") > -1 :

            buffer = self.clearbuffer(buffer)
            node = Node(self.nodeNum, NodeKind.SEQUENTIAL, None, buffer)
            self.add_node(node)

            if first == -1 and pre != None:
                pre.t = node
                first += 1
            else:
                self.add_edge(lastNode, node, EdgeKind("SEQUENTIAL"))

            next.t = self.nodeList[1]
            lastNode = node
            lastState = "RETURN"
        # else:
        #     buffer = self.clearbuffer(buffer)
        #     node = Node(self.nodeNum, NodeKind.SEQUENTIAL, None, buffer)
        #     self.add_node(node)
        #     # 新建节点时，若是第一个，继承mixedNode的pre边，否则与上一个节点建立边关系
        #     if first == -1 and pre != None:
        #         pre.t = node
        #         first += 1

        if next:
            next.f = lastNode
        # print("-----------End of gen_subflowgraph_from_code---------------")
        # self.show()
        pass
        return continueNodeNew,breakNodeNew

    def clearbuffer(self,t):

        t = t.replace("\n", "")
        t = t.replace("\t", "")
        t = t.replace("\r", "")
        # t = t.replace(" ", "")

        start = -1
        flag1 = False
        end = -1
        flag2 = False
        l = len(t)
        for j in range(l):
            if flag1:
                start = j - 1
                break
            if t[j] == " ":
                flag1 = False
            else:
                flag1 = True

        for k in range(l - 1, -1, -1):
            if flag2:
                end = k + 1
                break
            if t[k] == " ":
                flag2 = False
            else:
                flag2 = True
        if start > -1 and end > -1:
            t = t[start:end + 1]
        else:
            # print("ERROR: in buffer")
            pass

        return t

    def gen_node_embedding(self):

        for node in self.nodeList.values():
            if node!=None and node.kind.value != 5:
                index = node.index
                nodeKind = node.kind.value
                inDegree = len(node.connectedFrom)
                outDegree = len(node.connectedTo)
                label = 0
                if node.label == None:
                    label = 0
                else:
                    label = len(node.label)

                content = 0
                if node.content == None:
                    content = 0
                else:
                    content = len(node.content)

                self.nodeEmbedding.append([index,nodeKind,inDegree,outDegree,label,content])

    def add_node(self, node: Node):

        self.nodeList.update({node.index: node})
        self.nodeNum += 1

    def get_node(self, index):
        vertex = self.nodeList.get(index)
        return vertex

    def __contains__(self, index):
        return index in self.nodeList.values()

    def add_edge(self, f, t, weight: EdgeKind):


        # f, t = self.get_node(f), self.get_node(t)

        # if not f:
        #     self.add_node(f)
        # if not t:
        #     self.add_node(t)

        f.add_neighbor(t, weight)
        t.add_from(f,weight)

        e = Edge(f, t, weight)
        self.edgeList.update({self.edgeNum: e})
        self.edgeNum += 1
        return e

    def modify_edge_front(self,edge:Edge,node:Node):

        f = edge.f
        t = edge.t
        weight = edge.weight
        #replace f->t to node->t

        f.connectedTo.pop(t)

        t.connectedFrom.pop(f)
        t.connectedFrom.update({node: weight})

        return

    def modify_edge_tail(self,edge:Edge,node:Node):

        f = edge.f
        t = edge.t
        weight = edge.weight

        f.connectedTo.pop(t)
        f.connectedTo.update({node: weight})

        t.connectedFrom.pop(f)
        return

    def get_edge(self,index):
        return self.edgeList[index]

    def get_nodes(self):
        return self.nodeList.keys()

    def exist_mixed_node(self):
        for i in self.nodeList.keys():
            node = self.nodeList[i]
            if node.kind == NodeKind.MIXED:
                return True
        return False

    def __iter__(self):
        return iter(self.nodeList.values())

    def show(self):
        for i in self.nodeList.keys():
            print(f"node index is {i}, nodeKind is {self.nodeList[i].kind}, "
                  +f"label is {self.nodeList[i].label}, content is: \n{self.nodeList[i].content}")

        for i in self.edgeList.keys():
            print(f"edge index is {i}, edge is [{self.edgeList[i].f.index} -> {self.edgeList[i].t.index}] "
                  + f"weight is {self.edgeList[i].weight}")
        print(f"node embedding is {self.nodeEmbedding}")

    def toPYG(self):

        # data = Data(x=x, edge_index=edge_index)
        hash_map = {}
        c = 0
        for node in self.nodeList.values():
            if node!=None and node.kind.value != 5:
                index = node.index
                hash_map.update({index: c})
                c = c+1
        x = []
        for n in self.nodeEmbedding:
            x.append(n[1:len(n)])
        edge_index = []
        fedge = []
        tedge = []
        for i in self.edgeList.keys():
            fedge.append(hash_map.get(self.edgeList[i].f.index))
            tedge.append(hash_map.get(self.edgeList[i].t.index))
        edge_index.append(fedge)
        edge_index.append(tedge)
        # print(f"x is {x}")
        # print(f"edge is {edge_index}")
        edge_index = torch.tensor(edge_index, dtype=torch.long)
        x = torch.tensor(x, dtype=torch.float)
        data = Data(x=x, edge_index=edge_index)
        self.data = data
        return data



def gen_data_from_rs(fileName):

    content, strTable = generating_content(fileName)
    flowChart = Graph(content)
    flowChart.gen_flowchart()
    flowChart.gen_node_embedding()
    flowChart.toPYG()
    # flowChart.show()
    # print(flowChart.data.x,flowChart.data.edge_index)
    return flowChart.data

def gen_acfg_from_txt(file,index=0):

    # print("file is \n",file)
    content, strTable = generating_content_by_txt(file)
    # print("content is \n",content)
    flowChart = Graph(content)
    flowChart.gen_flowchart()
    flowChart.gen_node_embedding()
    flowChart.toPYG()
    # flowChart.show()
    # print(flowChart.data.x,flowChart.data.edge_index)
    return flowChart.data

def gen_nodes_from_rs(codeString):

    content, strTable = generating_content_by_txt(codeString)
    flowChart = Graph(content)
    flowChart.gen_flowchart()
    flowChart.gen_node_embedding()
    flowChart.toPYG()
    # flowChart.show()
    # print(flowChart.data.x,flowChart.data.edge_index)
    nodes = []
    for key,value in flowChart.nodeList.items():
        if value.kind !=NodeKind.MIXED and value.kind !=NodeKind.USED:
            nodes.append(value);
    return nodes


