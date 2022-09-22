
def add_noise(file: str, add_size=10):
    noise_list = []
    for i in range(add_size):
        noise_list.append(f"assert_eq!({i},{i});")
        # print(noise_list[i])
    file_list = []
    file_list.append(file)
    index = file.find("fn")
    # print(index)
    # print(file[index])
    start = -1
    for i in range(index, len(file)-1):
        if file[i] == "{":
            start = i + 1
            break
    for i in range(add_size):
        temp = ""
        temp = temp + file[0:start]
        temp = temp + noise_list[i]
        temp = temp + file[start:len(file)]
        file_list.append(temp)
        # print(temp)
        pass

    return file_list


if __name__ == "__main__":
    file = "#![allow(unused)]fn main() {let x: Result<u32, &str> = Ok(2);assert_eq!(unsafe { x.unwrap_unchecked() }, 2);}"
    l = add_noise(file)
    print(l)
