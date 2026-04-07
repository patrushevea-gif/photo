# Memorial Photo Pro

Полностью переработанный монорепозиторий B2B SaaS-сервиса для предпечатной подготовки фото под гравировальные станки.

## Структура

- `frontend/` — Next.js приложение (загрузка изображения, этапы AI-пайплайна, выбор станка, экспорт).
- `backend/` — FastAPI API с пайплайном обработки и промышленным `export/` модулем для станков.

## Backend

### Запуск

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Основные endpoint'ы

- `POST /pipeline/enhance`
- `POST /pipeline/remove-bg`
- `POST /pipeline/outfit`
- `POST /pipeline/mockup`
- `POST /export/machine`

## Тесты

```bash
python -m pytest -q
```
