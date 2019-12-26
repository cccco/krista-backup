# -*- coding: UTF-8 -*-

import os
import shutil
from collections import namedtuple
from datetime import datetime

from lib import yaml


class AppConfig():
    """Синглетон для хранения конфигурации приложения."""

    _config_filename = 'config.yaml'
    _config_default_path = '/opt/KristaBackup'
    _config = None

    _server_fullname = None
    _start_time = datetime.now()

    _filename_dateformat = '%Y%m%d_%H%M%S'
    _start_time_str = _start_time.strftime(
        _filename_dateformat)  # Для имени лога и создаваемых файлов
    # Для записей в логах используем формат, совпадающий с syslog: YYYY-MM-DD hh:mm:ss
    _log_dateformat = '%Y-%m-%d %H:%M:%S'

    @staticmethod
    def get_log_dateformat():
        try:
            if AppConfig._config is None:
                AppConfig.conf()
        except Exception:
            pass
        return AppConfig._log_dateformat

    @staticmethod
    def get_filename_dateformat():
        try:
            if AppConfig._config is None:
                AppConfig.conf()
        except Exception:
            pass
        return AppConfig._filename_dateformat

    @staticmethod
    def get_starttime():
        try:
            if AppConfig._config is None:
                AppConfig.conf()
        except Exception:
            pass
        return AppConfig._start_time

    @staticmethod
    def get_starttime_str():
        if AppConfig._config is None:
            AppConfig.conf()
        return AppConfig._start_time_str

    @staticmethod
    def set_task_name(task_name):
        if task_name not in AppConfig.conf().schedule:
            raise ConfigError(
                'Не задано задание в расписании файла конфигураций {0}'.format(
                    AppConfig._config_filename,
                )
            )
        else:
            AppConfig._schedule_name = task_name
        if 'project' not in AppConfig.conf().schedule[task_name].get(
            'naming',
            '',
        ) and AppConfig._project is None:
            raise ConfigError(
                'Не задан проект для задания в расписании файла конфигураций {0}'
                .format(AppConfig._config_filename),
            )
        elif 'project' in AppConfig.conf().schedule[task_name].get(
            'naming',
            '',
        ):
            AppConfig._project = AppConfig.conf().schedule[task_name].get('naming')[
                'project']
        if 'region' not in AppConfig.conf().schedule[task_name].get(
            'naming',
            '',
        ) and AppConfig._region is None:
            raise ConfigError(
                'Не задан регион для задания в расписании файла конфигураций {0}'
                .format(AppConfig._config_filename),
            )
        elif 'region' in AppConfig.conf().schedule[task_name].get(
            'naming',
            '',
        ):
            AppConfig._region = str(
                AppConfig.conf().schedule[task_name].get('naming')['region']
            )

    @staticmethod
    def get_server_name():
        if AppConfig._config is None:
            AppConfig.conf()

        return AppConfig._server_name

    @staticmethod
    def conf():
        if AppConfig._config is None:
            try:
                AppConfig._config = YamlConfigMapper(
                    AppConfig._config_default_path, AppConfig._config_filename)
            except ConfigError:
                AppConfig._config = YamlConfigMapper(os.getcwd(),
                                                     AppConfig._config_filename)

            AppConfig.parseConfig()
        return AppConfig._config.config

    @staticmethod
    def parseConfig():

        if 'date_format' in AppConfig.conf().logging.keys():
            AppConfig._date_format = AppConfig.conf().logging['date_format']
            AppConfig._start_time_str = datetime.strftime(
                AppConfig._filename_dateformat)

        if not 'server_name' in AppConfig.conf().naming.keys():
            raise ConfigError(
                'Не задано имя сервера в файле конфигурации {0}'.format(
                    AppConfig._config_filename,
                ),
            )
        else:
            AppConfig._server_name = AppConfig.conf().naming['server_name']

        # Cтандартное значение региона
        if 'region' in AppConfig.conf().naming.keys():
            AppConfig._region = str(AppConfig.conf().naming['region'])

        # Cтандартное значение проекта
        if 'project' in AppConfig.conf().naming.keys():
            AppConfig._project = AppConfig.conf().naming['project']


class YamlConfigMapper:
    """
        Класс YamlConfigMapper взаимодействует с файловой системой - читает файлы конфигураций в yaml
    """

    config_file_name = 'config.yaml'
    config = None

    def __init__(self, path, filename):
        self.config_file_name = filename

        if os.path.exists(self.config_file_name) and os.path.isfile(
                self.config_file_name):
            self.loadAll()
        else:
            self.config_file_name = os.path.join(path, filename)
            if os.path.exists(self.config_file_name) and os.path.isfile(
                    self.config_file_name):
                self.loadAll()
            else:
                raise ConfigError("Отсутствует файл конфигурации %s" %
                                  (self.config_file_name,))

    def getConf(self):
        return self.config

    def loadAll(self):
        with open(self.config_file_name, 'r') as stream:
            conf_dict = yaml.load(stream, Loader=yaml.FullLoader)
        self.config = namedtuple('Config',
                                 conf_dict.keys())(*conf_dict.values())

    def storeAll(self):
        if not os.path.exists('config_history'):
            os.mkdir('config_history')
        bk_filename = os.path.join(
            'config_history', '.'.join([
                self.config_file_name,
                datetime.now().strftime('%Y%m%d_%H%M%S')
            ]))
        shutil.copy(self.config_file_name, bk_filename)
        with open(self.config_file_name, 'w') as stream:
            yaml.dump(dict(self.config._asdict()),
                      stream=stream,
                      allow_unicode=True,
                      default_flow_style=False)


class ConfigError(Exception):

    def __init__(self, msg):
        if msg:
            self.message = msg
        else:
            self.message = u'Ошибка в конфигурации model.yaml'