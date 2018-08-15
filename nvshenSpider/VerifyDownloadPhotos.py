import os

base_file_path = "/Volumes/移动城堡/spider_data/nvshen_data"


def searching_files():
    index = 0
    for dir_path, dir_names, file_names in os.walk(base_file_path):
        for file_name in file_names:
            file_path = os.path.join(dir_path, file_name)
            if os.path.isfile(file_path) and not file_path.startswith("._"):
                index += 1
                if os.path.getsize(file_path) == 0:
                    print(index, "文件存在问题,已删除", file_path)
                    os.remove(file_path)
                else:
                    print(index, "文件校验通过")


def counter():
    count = 0
    index = 0
    for dir_path, dir_names, file_names in os.walk(base_file_path):
        count += len(file_names)
        print(index, dir_path)
        index += 1
    print("共", count)


if __name__ == "__main__":
    searching_files()
    counter()
