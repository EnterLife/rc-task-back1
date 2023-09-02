# Задача на должность junior-программист

# Описание данных

Даны стоимости проектов в млрд р по годам, число лет в данных может варьироваться.
Данные иерархические, то есть обладают структурой дерева, где иерархия показана
в колонке код.


# Описание задачи

1. Необходимо прочитать файл и преобразовать его с помощью библиотеки pandas следующим образом:
терминальные вершины дерева идут со значением по годам. Необходимо для нетерминальных вершин
вычислить (проект, подпроект) сумму по терминальным для каждого года.
2. Необходимо хранить данные в БД PostgreSQL. Соответственно, для этого необходимо составить DDL.
И написать код, который будет раскладывать данные в физическую модель.

Необходимо реализовать задачу при помощи pandas

# Описание решения

1. Файл main.py содержит основные классы и методы применяемые для решения задачи.
    Файл logger.py содержит класс и настройки логирования событий. События отображаются в консоли и записываются в файл log.txt
    Конфигурационный файл settings.ini содержит настройки для подключения к базе данных и глобальные настройки логгирования.
    Для логгирования на этапе разработки установлен режим debug = True, при котором отладочные сообщения выводятся в консоль и записываются в файл логов.

2. Решение состоит из двух классов: DataProcessor и DatabaseConnector.
    Класс DataProcessor используется для обработки данных из файла. В методе __init__ класса происходит чтение данных из файла и их конвертация в dataframe. Затем выполняются следующие действия:
    - Преобразование столбца 'код' в строковый тип данных.
    - Заполнение пустых значений в dataframe пустой строкой.
    - Создание нового dataframe new_data с нужными столбцами ('проект' и годы).

    Метод traverse_tree используется для обхода дерева данных. Для заданного кода и проекта получаем все дочерние узлы. Если узлов нет, то записываем проект и значения по годам в новый dataframe new_data. Если узлы есть, то рекурсивно вызываем traverse_tree для каждого узла.

    Метод process_data используется для вызова функции traverse_tree для каждого корневого кода.

    Класс DatabaseConnector используется для работы с базой данных. В методе __init__ класса сохраняются параметры подключения к базе данных. Затем выполняются следующие действия:
    - Создание таблицы projects в базе данных с нужными столбцами.
    - Вставка данных из new_data в таблицу projects.
3. В основной части кода происходит чтение конфигурационного файла и сохранение параметров. Затем создаются экземпляры классов DataProcessor и DatabaseConnector, и выполняется            последовательное выполнение методов для обработки данных и записи их в базу данных.
    Если происходит любая ошибка, то ведется запись ошибки в лог с подробным traceback и вызывается исключение.
    В конце кода выводится сообщение об успешном завершении.

# Как запустить предложенное решение

1. Скорректировать настройки базы данных в файле настроек settings.ini, указав корректные значения для полей:
    database_name = test_db,
    user = postgres,
    password = user,
    host = 127.0.0.1,
    port = 5432.
2. Файл с данными должен называться data.csv (имя можно изменить в файле настроек settings.ini изменив соответствующее поле data_file = data.csv).
    Файл с данными должен распологаться в корне папки проекта.
3. Установить виртуальное окружение при помощи setup_environment.bat.
4. Запустить приложение при помощи start.bat
