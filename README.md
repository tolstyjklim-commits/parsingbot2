# NFT Parser Bot — запуск на GitHub Actions

Бот работает через **long polling** (webhook на Actions невозможен) и перезапускает себя каждые 5 ч 40 мин.

## 1. Внешние базы (Actions ничего не хранит между запусками)
- **PostgreSQL** → Neon (neon.tech) или Supabase. Нужна строка подключения.
  Для Supabase берите *Session pooler / Direct* (порт 5432).
- **Redis** → Upstash (upstash.com). Нужна ссылка вида `rediss://default:...@...:6379`.

## 2. Репозиторий
Создайте **публичный** репозиторий и загрузите содержимое папки (включая `.github/`).

## 3. Секреты
Settings → Secrets and variables → Actions → New repository secret:

| Секрет | Значение |
|---|---|
| `BOT_TOKEN` | токен от @BotFather |
| `DATABASE_URL` | строка Postgres |
| `REDIS_URL` | строка Redis |
| `OPENAI_API_KEY` | ключ OpenAI |
| `PARSER_PROXIES` | прокси, по одному на строку: `http://user:pass@host:port` |
| `ADMIN_IDS` | (необязательно) id админов через запятую |

## 4. Запуск
Вкладка Actions → **Telegram NFT Bot** → Run workflow. Дальше всё идёт само.

## Важно
- Остановите старый деплой на Railway, иначе два экземпляра будут конфликтовать.
- Не добавляйте `WEBHOOK_HOST` — его наличие переключает бота обратно в режим webhook.
