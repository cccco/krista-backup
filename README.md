# KristaBackup

Система для автоматизации процесса создания, ротации и перемещения бэкапов.

Особенности:


1. Работает автономно


2. Имеет кросс-платформенную конфигурацию


3. Логирование во время выполнения: сокращённое и подробное


4. Интегрируема с системами мониторинга (например, Zabbix)

Поддерживаемые OS: Ubuntu 14.04 и выше, Debian 8 и выше, CentOS 7, AltLinux 8, Astra Linux 1.6
Для запуска требуется python3.5 и выше.

Документация в форматах html и текстовом расположена в папке docs.

# Установка


1. Клонировать репозиторий.

```
git clone https://github.com/javister/krista-backup
```

2. Скопировать проект в необходимую директорию. Обычно мы храним
приложение в каталоге /opt. Для установки в /opt могут
потребоваться права sudo.

```
cp KristaBackup/KristaBackup /opt/
```

3. Установить зависимости для базовой системы (без веб-интерфейса) из файла requirements.system.
Зависимости устанавливаются из репозиториев ОС. Для Debian и Ubunutu команда будет выглядеть так:

```
cd /opt/KristaBackup
sed 's/#.*//' requirements.system | xargs sudo apt-get install -y
```

3. Установить python-зависимости для веб-интерфейса с помощью утилиты pip.
Для того чтобы не менять окружение системы и соблюсти требуемую версионность,
лучше установить зависимости в тот же каталог, что и приложение,
использюя опцию --target.

```
cd /opt/KristaBackup
python3 -m pip install -r requirements.txt --target .
```

Назначаем владельца и права, если копировали/ставили зависимости не под root:

```
chown -R root:root /opt/KristaBackup
chmod -R 0755 /opt/KristaBackup/KristaBackup.py
chmod -R 0755 /opt/KristaBackup/UsersUtils.py
```

# Использование

Из командной строки можно:


* запустить сконфигурированное задание,


* добавить/удалить задание из cron,


* запустить веб-интерфейс или веб-api,


* отредактировать список пользователей веб-интерфейса.

Подробнее смотрите раздел "Использование" или docs/text/usage.txt

# Конфигурирование

Используемая терминология:

    
    * Действие (action) - выполнение какой-то конкретной команды, например, pg_dump или rsync.


    * Задание (task) содержит список действий, которые требуется выполнить в определенное время.


    * Конфгурации заданий сохраняются в разделе расписания (schedule).

    Задания могут быть активными или неактивными, активные задания прописаны в cron.
    Статус задания можно посмотреть в crontab или в веб-интерфейсе.

Конфигурации описываюстя в формате yaml, можно использовтать традиционный синтаксис с отступами
или json-нотацию со скобками. Примеры нотация в файлах config.yaml.example и config.yaml.example2.

Подробнее о конфигурировании можно прочитать в разделе "Конфигурация"
или docs/text/configuration.txt

Схематичный пример конфигурации:

```
schedule: # расписание
  full_dump: # задание
    actions: # действия в задании
      - some_action_1 # действие 1
      - some_action_2 # действие 2
    cron: 00 23 * * 1-6
    descr: вечером по будням выполняются some_action_1 и some_action_2

actions: #  список всех атомарных действий
  some_action_1: #  конфигурация действия 1
    type: type1

  some_action_2: #  конфигурация действия 2
    type: type2
```

# Разработчики

[s.postnikov@krista.ru](mailto:s.postnikov@krista.ru), [m.adrian@krista.ru](mailto:m.adrian@krista.ru)

# Лицензия

Copyright 2019 ООО НПО Криста

Licensed under the Apache License, Version 2.0
