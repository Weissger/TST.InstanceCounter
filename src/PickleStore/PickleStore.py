import pickle


class PickleStore(object):
    def __init__(self):
        self.__store = {}

    def store_instance_count(self, in_type, count):
        self.__store[in_type] = count

    def get_instance_count(self, in_type):
        if in_type in self.__store:
            return self.__store[in_type]
        else:
            return None

    def dump(self, path):
        with open(path, 'w+') as f:
            pickle.dump(self.__store, f)

    def load(self, path):
        with open(path) as f:
            self.__store = pickle.load(f)

