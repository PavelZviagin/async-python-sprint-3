# Доступные команды

    "/send <message> - send message to all users"
    "/send <username> <message> - send message to specific user"
    "/status - show online users"
    "/history - show last 20 messages"
    "/rename <new_username> - change your username"
    "/report <username> - report user"
    "/quit - disconnect from server"

# Проектное задание третьего спринта

Спроектируйте и реализуйте приложение для получения и обработки сообщений от клиента.

Кроме основного задания, выберите из списка дополнительные требования. У каждого требования есть определённая сложность, от которой зависит количество баллов. Необходимо выбрать такое количество заданий, чтобы общая сумма баллов была больше или равна `4`. Выбор заданий никак не ограничен: можно выбрать все простые или одно среднее и два простых, или одно продвинутое, или решить все.

## Описание задания

### `Сервер`

Реализовать сервис, который обрабатывает поступающие запросы от клиентов.

Условия и требования:
1. Подключенный клиент добавляется в «общий» чат, где находятся ранее подключенные клиенты.
2. После подключения новому клиенту доступны последние N cообщений из общего чата (20, по умолчанию).
3. Повторно подключенный клиент имеет возможность просмотреть все ранее непрочитанные сообщения до момента последнего опроса (как из общего чата, так и приватные).
4. По умолчанию сервер стартует на локальном хосте (127.0.0.1) и на 8000 порту (возможность задать любой).

<details>
<summary> Список возможных методов для взаимодействия (можно изменять) </summary>

1. Подключиться к общему чату.

```python
POST /connect
```

2. Получить статус и информацию о чатах.

```python
GET /status
```

3. Отправить сообщение в общий чат или определенному пользователю в приватный чат.

```python
POST /send
```
</details>


### `Клиент`

Реализовать сервис, который умеет подключаться к серверу для обмена сообщениями с другими клиентами.

Условия и требования:
1. После подключения клиент может отправлять сообщения в «общий» чат.
2. Возможность отправки сообщения в приватном чате (1-to-1) любому участнику из общего чата.


### Дополнительные требования (отметить [Х] выбранные пункты):

- [ ] (1 балл) Период жизни доставленных сообщений — 1 час (по умолчанию).
- [X] (1 балл) Клиент может отправлять не более 20 (по умолчанию) сообщений в общий чат в течение определенного периода — 1 час (по умолчанию). В конце каждого периода лимит обнуляется.
- [ ] (1 балл) Возможность комментировать сообщения.
- [ ] (2 балла) Возможность создавать сообщения с заранее указанным временем отправки; созданные, но не отправленные сообщения можно отменить.
- [X] (2 балла) Возможность пожаловаться на пользователя. При достижении лимита в 3 предупреждения, пользователь становится «забанен» — невозможность отправки сообщений в течение 4 часов (по умолчанию).
- [ ] (3 балла) Возможность отправлять файлы различного формата (объёмом не более 5Мб, по умолчанию).
- [ ] (3 балла) Возможность создавать кастомные приватные чаты и приглашать в него других пользователей. Неприглашенный пользователь может «войти» в такой чат только по сгенерированной ссылке и после подтверждения владельцем чата. 
- [ ] (4 балла) Пользователь может подключиться с двух и более клиентов одновременно. Состояния должны синхронизироваться между клиентами.
- [ ] **(5 баллов) Реализовать кастомную реализацию для взаимодействия по протоколу `http` (можно использовать `asyncio.streams`);


## Требования к решению

1. Опишите документацию по разработанному API.
2. Используйте концепции ООП.
3. Используйте аннотацию типов.
4. Предусмотрите обработку исключительных ситуаций.
5. Приведите стиль кода в соответствие pep8, flake8, mypy.
6. Логируйте результаты действий.


## Рекомендации к решению

1. Покройте написанный код тестами.
2. Можно использовать внешние библиотеки, но не фреймворки (описать в **requirements.txt** или иной системе управления зависимостями).
3. Можно не проектировать БД: информацию хранить в памяти и/или десериализовать/сериализировать в файл (формат на выбор) и восстанавливать при старте сервера.
4. Нет необходимости разрабатывать UI для клиента: можно выводить информацию в консоль или использовать лог-файлы.
5. API может быть реализовано, как вызов по команде/флагу (для консольного приложения) или эндпойнт (для http-сервиса).
