tmp_dir = 'C:/Users/belim/PycharmProjects/Accredited Certificate and CRL installer/temp'   # директория для временных файлов
crl_dir = 'C:/Users/belim/PycharmProjects/Accredited Certificate and CRL installer/temp'   # директория для загрузки CRL
remote_dir = '/home/application/crl_updater/'                                              # /srv/www/crypto/data/CRL директория для файлов данных с серверов
log_dir = 'C:/Users/belim/PycharmProjects/Accredited Certificate and CRL installer/'       # директория для хранения логов

log_name_mask = 'crl_cert_installer_%s.log'                                                # маска для названия файла лога
cert_mca_f_t = 'mCA_%s.txt'                                                                # маска для названия файлов данных с серверов

test_mode = True                                                                           # включение тестового режима (без установки)
language = 'ENG'                                                                           # выбор языка при логировании
server_list = [1, 2, 4, 5]                                                                 # доступные сервера
sleep_time = 1800                                                                          # время задержки выполнения, seconds

cert_install_tries = 3                                                                     # количество попыток установки сертификата
crl_install_tries = 3                                                                      # количество попыток установки CRL
install_timeout = 1                                                                        # время задержки между установками
