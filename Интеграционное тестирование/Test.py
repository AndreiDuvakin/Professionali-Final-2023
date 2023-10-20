from requests import post, get


def main_test():
    post('http://localhost:5001/util/1', data={"test": 1})
    post('http://localhost:5001/util/1', data={"test": 2})
    post('http://localhost:5001/util/1', data={"test": 3})
    post('http://localhost:5001/util/1', data={"test": 4})


if __name__ == '__main__':
    main_test()
