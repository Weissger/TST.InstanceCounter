import os
import urllib


class FileStore(object):
    def __init__(self, folder):
        self.__folder = folder
        if not os.path.isdir(folder):
            os.mkdir(folder)

    def store_instance_count(self, in_type, count):
        f = open(self.__folder + urllib.quote_plus(in_type) + ".txt", 'w+')
        f.write(str(count))
        f.close()

    def get_instance_count(self, in_type):
        path = self.__folder + urllib.quote_plus(in_type) + ".txt"
        if os.path.isfile(path):
            res = None
            f = open(self.__folder + urllib.quote_plus(in_type) + ".txt", 'r')
            for line in f:
                res = int(line)
            f.close()
            return res
        else:
            return None
