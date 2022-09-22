
import os

def del_file(path_data):
    for i in os.listdir(path_data):
        file_data = path_data + "\\" + i
        if os.path.isfile(file_data) == True:
            if "pre_filter.pt" in file_data or "pre_transform.pt" in file_data:
                os.remove(file_data)
        else:
            del_file(file_data)

def del_pre_file():
    path_data = r"..\database\processed"

    del_file(path_data)

if __name__=="__main__":
    path_data = r"..\database\processed"
    del_file(path_data)

