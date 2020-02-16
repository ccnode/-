import time, hashlib


def create_id():
    m = hashlib.md5()
    m.update(bytes(str(time.perf_counter()), encoding='utf-8'))
    return m.hexdigest()


if __name__ == '__main__':
    print(create_id())