from .SparqlInterface.src.ClientFactory import make_client
from .SparqlInterface.src.Interfaces.AbstractClient import AbstractClient
from .SQLiteStore.InstanceCountStore import InstanceCountStore
from .Utilities.Logger import log
from .Utilities.Utilities import log_progress
from .NTripleLineParser.src.NTripleLineParser import NTripleLineParser
from sqlite3 import IntegrityError
from datetime import datetime
import gevent


def get_count(in_type=None, server=None, store=None):
    """
    :param in_type:
    :param server:
    :type server: AbstractClient
    :param store:
    :type store: InstanceCountStore
    :return:
    """
    return server.count_instances(in_type)


class InstanceCounter(object):
    def __init__(self, server=None, user=None, password=None, n_processes=None, sqlite_db='./data/instance_count.db',
                 log_level="INFO"):
        log.setLevel(log_level)
        self.nt_parser = NTripleLineParser(" ")
        self.__store = InstanceCountStore(sqlite_db)
        self.__server = make_client(server, user, password)
        self.number_of_processes = n_processes

    def count_all_instances(self, in_file=None):
        cur_time = datetime.now()
        if in_file:
            log.info("Counting with classes from file")
            self.use_file_for_classes(in_file)
        else:
            log.info("Counting with classes from service")
            self.use_service_for_classes()
        log.info("Done in: " + str(datetime.now() - cur_time))

    def use_file_for_classes(self, f):
        with open(f) as input_file:
            tmp_classes = set()

            for line_num, line in enumerate(input_file):
                triple = self.nt_parser.get_triple(line)
                if not triple:
                    continue
                log_progress(line_num, 100)
                tmp_classes.add(triple['subject'])
                tmp_classes.add(triple['object'])
                if len(tmp_classes) >= self.number_of_processes-1:
                    threads = [gevent.spawn(self.__get_count, t) for t in tmp_classes]
                    tmp_classes = set()
                    gevent.joinall(threads)
                    for t in threads:
                        try:
                            self.__store.store_instance_count(t.value[0], t.value[1])
                        except IntegrityError as e:
                            pass
                    threads = []
            if len(tmp_classes) > 0:
                gevent.joinall(threads)
                for t in threads:
                    if t.value:
                        try:
                            self.__store.store_instance_count(t.value[0], t.value[1])
                        except IntegrityError as e:
                            pass

    def use_service_for_classes(self):
        log.critical("Counting with classes from service currently not supported.")
        pass

    def __get_count(self, in_type):
        return in_type, self.__server.count_instances(in_type)

    # def __spawn_daemon(self, target, kwargs):
    #     # Todo Event based?
    #     # Check every 0.1 seconds if we can continue
    #     if hasattr(self, "processManager"):
    #         while not self.processManager.has_free_process_slot():
    #             time.sleep(0.1)
    #
    #     p = Process(target=target, kwargs=kwargs)
    #     p.daemon = True
    #     if hasattr(self, "processManager"):
    #         try:
    #             self.processManager.add(p)
    #         except OccupiedError as e:
    #             log.critical(e)
    #             return 2
    #         else:
    #             p.start()
    #     else:
    #         p.start()
