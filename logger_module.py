# модуль инициации логгера
import logging
import ets.ets_log_preformat_lib as l_p


def init_log_config(log_file):

    # описываем формат лога
    logging.basicConfig(format=l_p.LOG_FORMAT_1,
                        datefmt=l_p.DATE_FORMAT_4,
                        level=logging.INFO,
                        filename=log_file)

    logging.getLogger("paramiko.transport").setLevel(logging.ERROR)
    logging.getLogger("requests").setLevel(logging.ERROR)


# описываем функцию, которая будет возвращать логгер с нужным именем
# (названием главной функции, в которой произошло событие)
def logger(logger_name):
    return logging.getLogger(logger_name)
