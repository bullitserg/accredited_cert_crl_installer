from config import language

translations = {
    'ENG': {'new_cert_info_found': 'New certificate found',
            'installing_crl': 'Installing crl',
            'cant_download_crl': 'Error download CRL (%(crlUrl)s): %(download_error)s',
            'crl_successfully_download': 'CRL successfully download (%(crlUrl)s) ',
            'crl_successfully_installed': 'CRL successfully installed (%(installation_info)s)',
            'crl_error_installed': 'Error CRL installation: (%(installation_info)s)',
            'installing_certificate': 'Installing certificate %(location)s',
            'certificate_successfully_installed': 'Certificate successfully installed (%(installation_info)s)',
            'certificate_error_installed': 'Error certificate installation (%(installation_info)s)'},

    'RUS': {'new_cert_info_found': 'Обнаружен новый сертификат',
            'installing_crl': 'Установка CRL',
            'cant_download_crl': 'Ошибка загрузки CRL (%(crlUrl)s): %(download_error)s',
            'crl_successfully_download': 'CRL успешно загружен (%(crlUrl)s) ',
            'crl_successfully_installed': 'CRL успешно установлен (%(installation_info)s)',
            'crl_error_installed': 'Ошибка установки CRL: (%(installation_info)s)',
            'installing_certificate': 'Установка сертификата %(location)s',
            'certificate_successfully_installed': 'Сертификат успешно установлен (%(installation_info)s)',
            'certificate_error_installed': 'Ошибка установка сертификата (%(installation_info)s)'}
}


def log_add(key):
    return ' '.join(['''%(sha1Hash)s # ''', str(translations[language][key])])

