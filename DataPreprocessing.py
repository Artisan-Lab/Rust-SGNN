# import unittest
import time




def read_file_to_str(fileName: str) -> str:
    try:
        f = open(fileName, "r")
        # print("__read file__")
        # print("fileName :\t{}".format(fileName))
        try:
            count = 0

            while True:
                content = f.readlines()

                count = count + 1
                # print("------count is {}-------\n".format(count))
                # print(content)
                if len(content) == 0:
                    break
                else:
                    resultStr = ""
                    for i in range(len(content)):
                        resultStr += content[i]
                    # print("content of file is:\n\t{}".format(resultStr))
                time.sleep(0.1)
                # print("content of file is:\n\t{}".format(content))
        finally:
            f.close()
            # print("__close file__")

    except Exception as result:
        print("error{}".format(result))

    return resultStr



class SymbolStack(object):
    top: int
    stack: list
    length: int

    def __init__(self):
        top = -1
        stack: list = []
        length = len(stack)

    def push(self, elem):
        if self.length > self.top + 1:
            self.top = self.top + 1
            self.stack[self.top] = elem
        else:
            self.top = self.top + 1
            self.stack.append(elem)
            self.length = len(self.stack)

    def pop(self):
        elem = self.stack[self.top]
        self.top = self.top - 1
        return elem

    pass


def delete_annotation(content):

    newContent = ''
    flag = 0
    delta = 0
    for i in range(len(content)):
        c = content[i]
        cNext: str

        if i + 1 < len(content):
            cNext = content[i + 1]
        else:
            cNext = None


        if c == '/' and cNext == '/' and flag == 0:
            flag = 1
        elif c == '/' and cNext == '*' and flag == 0:
            flag = 2


        if flag == 1 and c == '\n':
            delta = 1
            flag = 0
        elif flag == 2 and c == '*' and cNext == '/':
            delta = 2
            flag = 0


        if flag == 0:
            if delta == 0:
                newContent = newContent + c
            elif delta >= 1:
                delta = delta - 1
                pass

    return newContent



def replace_quotation_marks(content):
    finalContent = ''
    stringVariableTable = {}
    variableName = None
    value = ''

    flag = 0
    delta = 0
    for i in range(len(content)):
        c = content[i]
        cPre: str
        cNext: str
        if i > 0:
            cPre = content[i - 1]
        else:
            cPre = None


        if i + 1 < len(content):
            cNext = content[i + 1]
        else:
            cNext = None

        if c == '"' and flag == 0 and cPre != "\\" and delta == 0:
            flag = 1


        if flag == 1 and cNext == '"' and c != "\\":
            flag = 0
            delta = 2


        if flag == 0:
            if delta == 0:
                finalContent = finalContent + c
            elif delta >= 1:
                delta = delta - 1
                pass


        if flag + delta > 0:

            value = value + c
        if delta == 1:
            value = value + cNext
            variableName = "str" + str(len(stringVariableTable))
            stringVariableTable[variableName] = value
            value = ''
            finalContent = finalContent + "/*" + variableName + "*/"

    return finalContent, stringVariableTable



def generating_content(fileName: str):

    c1 = read_file_to_str(fileName)
    c2 = delete_annotation(c1)
    content, strTable = replace_quotation_marks(c2)
    return content, strTable

def generating_content_by_txt(file: str):

    c2 = delete_annotation(file)
    content, strTable = replace_quotation_marks(c2)
    return content, strTable



