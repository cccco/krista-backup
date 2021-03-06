.. _move_bkp_period:

MoveBkpPeriod
=============

Выполняет копирование всех выходных файлов из действий в
``action_list`` в директорию ``dest_path``. Копируются
файлы только последнего бэкапа.

В ``action_list`` могут быть действия типа ``Archiver`` (``zip``, ``tar``)
и ``pgdump``.

Параметры:
~~~~~~~~~~

.. csv-table::
   :widths: 15, 30, 20
   :header: "название", "описание", "значение"

   "dest_path","Каталог для файлов с результатом.", "путь к директории"
   "periods", "список с периодами", "{ } (см. пример)"
   "action_list", "список имён действий, результаты которых требуется скопировать", "[ ]"
   "dry", "Не выполнять копирование файлов (dryrun).", "false (стандартное значение)"

Пример:
~~~~~~~

.. code-block:: yaml

  mv_backup:
    action_list:
        - make_full_etc
        - make_full_opt
    periods:
        weekly:
            # path примет значение weekly
            cron: '40 02 * * 0'
        monthly:
            path: month
            cron: '40 02 * 1 *'
            max_files: 3
    dest_path: /backup/vault/
    descr: копирование бэкапов
    type: move_bkp_period

  make_full_etc:
    basename: etc
    src_path: /etc
    dest_path: /backup
    level: 0
    descr: бэкап файлов /etc 0-го уровня
    checksum_file: true
    source: make
    type: tar

  make_full_opt:
    basename: opt
    src_path: /opt
    dest_path: /backup
    level: 0
    descr: бэкап файлов /opt 0-го уровня
    source: make
    type: tar

Примечание:
~~~~~~~~~~~

Параметр ``cron`` в периоде не создаёт запись в ``crontab``, а
проверяет время запуска текущего задания. То есть, если период
имеет атрибут ``cron: '40 02 * * 0'``, то выполнение этого периода произойдёт,
если задание запущено в воскресенье в 2:40.

``Cleaner`` поддерживает наследование от ``MoveBkpPeriod`` и выполняет
очистку отдельно для каждого периода. Параметры для очистки можно задать напрямую
в действии (в примере: ``max_files`` в ``monthly``), либо их можно задать в
``cleaner``, сохраняя структуру ``period``.
