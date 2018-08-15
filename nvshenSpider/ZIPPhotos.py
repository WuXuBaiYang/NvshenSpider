from concurrent.futures import ThreadPoolExecutor
import zipfile
import os

start_path = "/Volumes/移动城堡/spider_data/nvshen_data/"
target_path = "/Volumes/移动城堡/spider_data/nvshen_data_zip"


def zip_dir(start_file, target_file, index):
    """
    文件夹压缩
    :param start_file:
    :param target_file:
    :param index:
    :return:
    """
    z = zipfile.ZipFile(target_file, 'w', zipfile.ZIP_DEFLATED)
    for dpath, dnames, fnames in os.walk(start_file):
        fpath = dpath.replace(start_file, '')
        fpath = fpath and fpath + os.sep or ''
        for fname in fnames:
            z.write(os.path.join(dpath, fname), fpath + fname)
        print(index, '已压缩', target_file)
    z.close()


if __name__ == "__main__":
    index = 0
    with ThreadPoolExecutor(18) as executor:
        for dir_path, dir_names, file_names in os.walk(start_path):
            if dir_path.endswith("/"):
                continue
            index += 1
            target_file = "%s%s.zip" % (target_path, dir_path[dir_path.rindex("/"):])
            if not os.path.exists(target_file):
                if len(file_names) > 0:
                    executor.submit(zip_dir, dir_path, target_file, index)
                    print(index, "正在压缩", target_file)
                else:
                    print(index, "文件夹为空")
            else:
                print(index, "文件已存在")
            break
        executor.shutdown()
        print("全部处理完成")
