.. _move_bkp_period:

MoveBkpPeriod
=============

Выполняет копирование файлов из ``src_path`` в ``dest_path``
по ``basename_list``.

Параметры:
~~~~~~~~~~

.. csv-table::
   :widths: 15, 30, 20
   :header: "название", "описание", "значение"

   "src_path", "исходная директория, в которой находятся файлы из basename из basename_list", ""
   "dest_path", "результирующая директория", ""
   "periods", "список с периодами", "пример значения можно увидеть ниже"
   "basename_list", "список из basename, которые требуется скопировать", "[] (стандартное значение)"

Пример:
~~~~~~~

.. code-block:: yaml

  mv_backup:
    descr: копирование бэкапов
    basename_list:
        - 'etc'
        - 'home_user'
    period:
        weekly:
            # path примет значение weekly
            cron': '40 02 * * 0'
        monthly:
            path: month
            cron': '40 02 * 1 *'
            max_files: 3
        src_path: /backup/0/
        dest_path: /backup/vault/
        type: move_bkp_period

Примечание:
~~~~~~~~~~~

``Cleaner`` поддерживает наследование от ``MoveBkpPeriod`` и выполняет
очистку отдельно для каждого периода. Параметры для очистки можно задать напрямую
в действии (в примере: ``max_files`` в ``monthly``), либо их можно задать в
``cleaner``, сохраняя структуру ``period``.