# Приложение для составления списка дел

Это REST API для бронирования столиков в ресторане.

Функционал:

- Просмотр всех столиков
- Создание столиков с указанием названия, количества мест, расположение 
- Удаление столиков по id, с проверкой если столик не зарезервирован
- Просмотр всех броней
- Создание брони с указанием имени заказчика, id столика, дата и время бронирования, на сколько минут забронирован столик
- удаление броней по id

Установка:

1. Клонируйте репозиторий:


2. Установите зависимости:

```bash
pip install -r requirements.txt
```

3. Запустите приложение:

```bash
cd app
uvicorn main:app --reload
```

4. API будет доступно на http://localhost:8000/docs с автоматической документацией Swagger.

