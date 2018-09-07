import argparse
import wget
from os.path import normpath, join
from itertools import count
from time import sleep
from ets.ets_mysql_lib import MysqlConnection as Mc
from ets.ets_certmanager_logs_parser_v2 import CertmanagerFile, get_info_file, STORE_MCA, FILE_MCA
from ets.ets_certmanager_logs_parser_v2 import install_certificate, install_crl
from queries import *
from config import *
from logger_module import *
from languages import *

PROGNAME = 'CRL and certificate installer'
DESCRIPTION = '''Скрипт для установки новых сертификатов и CRL из xml файла'''
VERSION = '1.0'
AUTHOR = 'Belim S.'
RELEASE_DATE = '2018-09-06'


def show_version():
    print(PROGNAME, VERSION, '\n', DESCRIPTION, '\nAuthor:', AUTHOR, '\nRelease date:', RELEASE_DATE)


# обработчик параметров командной строки
def create_parser():
    parser = argparse.ArgumentParser(description=DESCRIPTION)

    parser.add_argument('-v', '--version', action='store_true',
                        help="Показать версию программы")

    parser.add_argument('-s', '--server', type=int, choices=server_list,
                        help="Установить номер сервера")
    return parser

tmp_dir = normpath(tmp_dir)
crl_dir = normpath(crl_dir)
cn_cert = Mc(connection=Mc.MS_CERT_INFO_CONNECT)


def crl_install_lf(server, info):
    # функция установки CRL
    log_add('working_crl') % info
    # устанавливаем счетчик попыток установки
    crl_counter = count(start=crl_install_tries, step=-1)
    crl_file_location = join(crl_dir, str(rec['sha1Hash']) + '_' + server + '.crl')
    # пробуем загрузить файл по ссылке
    try:
        wget.download(info['crlUrl'], out=crl_file_location)
        logger.info(log_add('crl_successfully_download') % info)
    except Exception as crl_err:
        info['download_error'] = crl_err
        logger.info(log_add('cant_download_crl') % info)
        return

    # устанавливаем CRL
    info['crl_file_location'] = crl_file_location
    log_add('install_crl') % info
    installation_info = []
    while next(crl_counter):
        crl_install_status, crl_install_error = install_crl(server, crl_file_location,
                                                            is_local=False, test_mode=test_mode)

        installation_info.append('OK' if crl_install_status else str(crl_install_error))
        sleep(install_timeout)

    info['installation_info'] = ', '.join(installation_info)

    # если была хоть одна успешная попытка установки, то указываем что все ок
    if 'OK' in installation_info:
        logger.info(log_add('crl_successfully_installed') % info)
    else:
        logger.info(log_add('crl_error_installed') % info)
    return 0


def cert_install_lf(server, info):
    # функция установки сертификата
    logger.info(log_add('installing_certificate') % info)

    # устанавливаем счетчик попыток установки
    cert_counter = count(start=cert_install_tries, step=-1)
    installation_info = []

    # устанавливаем сертификат
    while next(cert_counter):
        cert_install_status, cert_install_error = install_certificate(server, info['location'],
                                                                      store=STORE_MCA, is_local=False,
                                                                      test_mode=test_mode)

        installation_info.append('OK' if cert_install_status else str(cert_install_error))
        sleep(install_timeout)

    info['installation_info'] = ', '.join(installation_info)

    # если была хоть одна успешная попытка установки, то указываем что все ок
    if 'OK' in installation_info:
        logger.info(log_add('certificate_successfully_installed') % info)
    else:
        logger.info(log_add('certificate_error_installed') % info)

    return 0

if __name__ == '__main__':
        # парсим аргументы командной строки
        my_parser = create_parser()
        namespace = my_parser.parse_args()

        if namespace.version:
            show_version()
            exit(0)

        if namespace.server:
            try:
                # инициируем лог-файл
                log_file = join(normpath(log_dir), log_name_mask % namespace.server)
                init_log_config(log_file)
                logger_name = 'SERVER_%s' % namespace.server
                logger = logger(logger_name)

                logger.info('Starting (server %s, waiting %s)' % (namespace.server, sleep_time))

                while True:
                    # загружаем данные об установленных сертификатах
                    mca_file = get_info_file(1, file_type=FILE_MCA, remote_dir=remote_dir)
                    mca_file_o = CertmanagerFile(mca_file)

                    # получаем сведения о сертификатах из последней версии файла
                    with cn_cert.open():
                        accredited_info = cn_cert.execute_query(get_accredited_info_query, dicted=True)

                    for rec in accredited_info:
                        # проверяем по хешу наличие сертификата на сервере
                        installed_cert = mca_file_o.get_info(SHA1Hash=rec['sha1Hash'])
                        # если сведения о сертификате из файла отсутствуют на сервере, то устанавливаем
                        if not installed_cert:
                            logger.info(log_add('new_cert_info_found') % rec)

                            cert_install_lf(namespace.server, rec)
                            crl_install_lf(namespace.server, rec)

                    sleep(sleep_time)

            # если при исполнении будут исключения - кратко выводим на терминал, остальное - в лог
            except Exception as e:
                logger.fatal('Fatal error! Exit', exc_info=True)
                print('Critical error: %s' % e)
                print('More information in log file')
                exit(1)
        else:
            show_version()
            print('For more information run use --help')

exit(0)

