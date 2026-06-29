# Telegram Mail Bot 📧🤖

Telegram бот с интеграцией Mail.ru почты. Анализ писем, отслеживание изменений, напоминания и уведомления.

## Возможности ✨

- 📧 Подключение Mail.ru аккаунта через App Password
- 📬 Получение и анализ писем
- 🔔 Уведомления о новых письмах в Telegram
- 📊 Отслеживание изменений в письмах
- ⏰ Напоминания о важных письмах
- 🏷️ Фильтры и категории писем
- 📈 Статистика по письмам
- 💾 Сохранение данных в PostgreSQL

## Технологический стек 🛠️

- **Python 3.9+**
- **aiogram 3.x** - Telegram Bot Framework
- **aiosmtplib** - работа с SMTP
- **SQLAlchemy** - ORM для БД
- **PostgreSQL** - база данных
- **APScheduler** - планировщик задач
- **python-dotenv** - управление переменными окружения
- **Railway** - хостинг

## Быстрый старт 🚀

### Локальное разворачивание

```bash
# Клонируйте репозиторий
git clone https://github.com/kaygrin00-hub/ai-sales-assistant.git
cd ai-sales-assistant

# Создайте виртуальное окружение
python -m venv venv
source venv/bin/activate

# Установите зависимости
pip install -r requirements.txt

# Скопируйте .env файл
cp .env.example .env

# Отредактируйте .env с вашими данными
# Запустите бота
python main.py
```

### Разворачивание на Railway

1. Перейдите на [railway.app](https://railway.app)
2. Создайте новый проект
3. Подключите этот GitHub репозиторий
4. Добавьте PostgreSQL сервис
5. Установите переменные окружения
6. Деплойте!

## Команды бота 🤖

- `/start` - начало работы
- `/help` - справка
- `/connect` - подключить Mail.ru аккаунт
- `/disconnect` - отключить аккаунт
- `/check` - проверить новые письма
- `/stats` - статистика
- `/settings` - настройки

## Структура проекта 📁

```
├── main.py                 # Точка входа
├── requirements.txt        # Зависимости
├── .env.example           # Пример переменных
├── Dockerfile             # Docker контейнер
├── railway.toml           # Конфиг Railway
├── bot/
│   ├── config.py          # Конфигурация
│   ├── core.py            # Основной класс бота
│   ├── handlers/          # Обработчики команд
│   ├── services/          # Бизнес-логика
│   └── keyboards/         # Клавиатуры
├── mail/
│   ├── connector.py       # Подключение к Mail.ru
│   ├── analyzer.py        # Анализ писем
│   └── fetcher.py         # Получение писем
├── db/
│   ├── models.py          # Модели SQLAlchemy
│   └── session.py         # Сессии БД
└── scheduler/
    └── tasks.py           # Фоновые задачи
```

## Установка Mail.ru App Password 🔐

1. Перейдите в [личный кабинет Mail.ru](https://account.mail.ru)
2. В меню выберите **Безопасность** → **Пароли приложений**
3. Создайте новый пароль для Telegram
4. Используйте этот пароль при подключении

## Лицензия 📄

MIT License

---

**Готово к использованию! 🎉**