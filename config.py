"""
Конфигурация бота
"""
import os
import re

try:  # локальный запуск: подхватываем .env, в GitHub Actions переменные уже в окружении
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass
from typing import List, Set

def _split_env_list(name: str) -> List[str]:
    """Читает список из переменной окружения (разделители: перенос строки, запятая, пробел)"""
    raw = os.getenv(name, "")
    return [p.strip() for p in re.split(r"[\n,;\s]+", raw) if p.strip()]


# ============================================================================
# TELEGRAM BOT
# ============================================================================

# Telegram токен бота
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

# Webhook настройки
WEBHOOK_HOST = os.getenv("WEBHOOK_HOST", "")
WEBHOOK_PATH = f"/bot/{BOT_TOKEN}"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# Веб-сервер
WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = int(os.getenv("PORT", 8080))


# ============================================================================
# REDIS
# ============================================================================

REDIS_URL = os.getenv("REDIS_URL", "")

# ============================================================================
# ADMIN
# ============================================================================

# ID администраторов (замените на свои)
_DEFAULT_ADMIN_IDS: Set[int] = {
    8354719175,  # Ваш Telegram ID
    8505715171,
}
# Можно переопределить секретом ADMIN_IDS (id через запятую/пробел/перенос строки)
_env_admins = {int(x) for x in _split_env_list("ADMIN_IDS") if x.lstrip("-").isdigit()}
ADMIN_IDS: Set[int] = _env_admins or _DEFAULT_ADMIN_IDS

# ============================================================================
# DATABASE
# ============================================================================

DATABASE_URL = os.getenv("DATABASE_URL", "")

if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL не установлен! Добавьте его в GitHub Secrets (Settings → Secrets and variables → Actions).")

# Некоторые провайдеры отдают postgres://, но asyncpg требует postgresql://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

print(f"✅ Используется PostgreSQL")

# ============================================================================
# PARSER
# ============================================================================

# Игнорируемые username при парсинге
IGNORE_USERNAMES: Set[str] = {
    "giftstoportals",
    "giftrelayer",
    "telegram",
    "durov",
    "giftstoportals",
    "giftrelayer",
    "Major_Speakers",
    "mrktbank",
    "gemsrelayer",
    "gifts_tester",
    "",
}

# Настройки парсера
PARSER_API_URL = "https://peek.tg/api/nft/gifts/search"
PARSER_REQUEST_DELAY = 1.0  # секунды между запросами
PARSER_MAX_CONCURRENT = 30  # максимум одновременных запросов
PARSER_MAX_PAGES = 20  # максимум страниц для парсинга
PARSER_RANGE_SIZE = 2000  # размер диапазона для рандомного парсинга

# Прокси (опционально)
# Список прокси берётся из секрета PARSER_PROXIES (по одному на строку):
#   http://user:pass@host:port
# НЕ храните логины/пароли прокси в коде - репозиторий для GitHub Actions публичный.
 # Прокси (отключены)
PARSER_PROXIES: List[str] = _split_env_list("PARSER_PROXIES")

PARSER_PROXY_FILE = None  # Или путь к файлу с прокси

# ============================================================================
# GPT FILTER
# ============================================================================

# OpenAI API ключ
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Модель GPT
GPT_MODEL = "gpt-4o-mini"  # или "gpt-4o", "gpt-3.5-turbo"

# Настройки фильтрации
GPT_TEMPERATURE = 0.3
GPT_MAX_TOKENS = 1000
GPT_BATCH_SIZE = 300  # максимум username в одном запросе

# Количество результатов по умолчанию
DEFAULT_FEMALE_COUNT = 30

# ============================================================================
# RATE LIMITING
# ============================================================================

# Лимиты для пользователей (запросов в минуту)
USER_RATE_LIMIT = 5

# Максимальное количество задач в очереди
MAX_QUEUE_SIZE = 200
NUM_WORKERS = 10

# ============================================================================
# MESSAGES
# ============================================================================

MESSAGES = {
    "start": """👋 Привет! Я бот для парсинга NFT подарков Telegram.

Выберите действие:""",
    
    "help": """ℹ️ **Помощь**

**Рандомный парсинг** - парсит случайную коллекцию и находит владельцев подарков

**Женские аккаунты** - выбираете коллекцию, бот парсит подарки и с помощью GPT находит женские username

**Как это работает:**
1. Бот парсит подарки из выбранной коллекции
2. Извлекает username владельцев
3. GPT анализирует username и определяет пол
4. Вы получаете список женских аккаунтов

⚠️ Ограничения: {rate_limit} запросов в минуту""",
    
    "select_collection": "Выберите коллекцию:",
    
    "parsing_started": "Парсинг начат... Это может занять некоторое время. Не надо хуярить в меня кучу запросов",
    
    "parsing_random": "Парсинг случайной коллекции: **{collection}**\n Ожидайте...",
    
    "parsing_female": "Парсинг коллекции **{collection}** для поиска женских аккаунтов\n Ожидайте...",
    
    "parsing_complete": """✅ **Парсинг завершён!**

📊 Коллекция: {collection}
👥 Найдено владельцев: {total}
⏱ Время: {time:.1f}с

{results}""",
    
    "parsing_female_complete": """✅ **Поиск завершен!**

📊 Коллекция: {collection}
👥 Всего владельцев: {total}
👩 Всего аккаунтов: {female_count}
⏱ Время: {time:.1f}с

{results}""",
    
    "parsing_error": "❌ Ошибка при парсинге: {error}",
    
    "no_results": "😔 Владельцы не найдены",
    
    "queue_full": "⚠️ Очередь переполнена. Нехуй спамить.",
    
    "rate_limit": "⏳ Слишком много запросов. Подожди.",
    
    "admin_only": "Эта команда доступна только администраторам",
}

# Кнопки
BUTTONS = {
    "random_parsing": "Рандомный парсинг",
    "female_accounts": "Женские аккаунты",
    "help": "❓ Помощь",
    "back": "На главную",
    "admin_panel": "⚙️ Админ панель",
    "stats": "Статистика",
    "broadcast": "Рассылка",
    "filter_parsing": "Парсинг по фильтрам",
    "proxy": "Прокси",
}







