# -*- coding: utf-8 -*-


INFINITY_PROCESS = '/bin/sh -c "trap : TERM INT; sleep infinity & wait"'

ENV = [
    'PYTHONIOENCODING=utf8',
    'LANG=ru_RU.utf8',
]

CONTAINERS_OPTS = {
    str(version): {
        'docker_image': 'snakepacker/python:3.{v}'.format(v=version),
        'link': '/usr/bin/KristaBackup',
        'prepared': None,
    }
    for version in range(2, 6)
}


class Tools(object):

    @staticmethod
    def get_trigger_value_from_container(container):
        _, output = container.exec_run(
            'cat /etc/zabbix/backup.trigger',
        )
        output = output.decode('utf-8')
        return output

    @staticmethod
    def clear_trigger(container):
        container.exec_run(
            'sh -c "echo -n \'\' > /etc/zabbix/backup.trigger"',
        )

    @staticmethod
    def check_trigger_success(container):
        return Tools.get_trigger_value_from_container(container) == 'SUCCESS'

    @staticmethod
    def check_trigger_warning(container):
        return Tools.get_trigger_value_from_container(container) == 'WARNING'

    @staticmethod
    def check_trigger_error(container):
        return Tools.get_trigger_value_from_container(container) == 'ERROR'


class Strategies(object):
    @staticmethod
    def run_full_dump_default(container):
        _, output = container.exec_run(
            'KristaBackup run make_full_dump_default --verbose',
        )
        output = output.decode('utf-8').split('\n')
        return 'INFO root Выполнено действие' in output[-2]

    @staticmethod
    def run_inc_dump_default(container):
        _, output = container.exec_run(
            'KristaBackup run make_diff_dump_default --verbose',
        )
        output = output.decode('utf-8').split('\n')
        Tools.get_trigger_value_from_container(container)
        return 'INFO root Выполнено действие' in output[-2]
