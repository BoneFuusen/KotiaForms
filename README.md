# KotiaForms

### Проект сделан в рамках тестового задания Student Labs 2024

KotiaForms - это проект по реализации backend-части сервиса-аналога GoogleForms и Яндекс Формы.

Инструментарий, использованный при создании проекта:
1) `FastAPI` - быстрый, удобный асинхронный фреймворк для создания API
2) `FastAPI-users` - лёгкий в использовании, кастомизируемый модуль для `FastAPI`. (Авторизация выполняется с помощью JWT + Cookie)
3) `SQLAlchemy` - библиотека для работы с реляционными СУБД
4) `PostgreSQL` + `asyncpg` - наиболее часто используемая СУБД в Enterprise разработке. Давно поддерживается, имеет широкую пользовательскую базу а также много библиотек на python для улучшения работы с ней.
5) `Pydantic` - удобная библиотека для валидации и преобразования данных.
6) `Alembic` - библиотека для миграции БД
7) `Uvicorn` - ASGI веб-сервер для локального запуска API

Ссылка на коллекцию Postman: https://elements.getpostman.com/redirect?entityId=34872755-b8765079-1d7c-42e9-9e10-8ee8f2ff7aec&entityType=collection

### Создатель проекта - Котов Сергей Владимирович, ОмГТУ, факультет ФИТиКС, кафедра ПМИФИ, группа ФИТ-222.