# Memorial Photo Pro

Полностью переработанный монорепозиторий B2B SaaS-сервиса для предпечатной подготовки фото под гравировальные станки.

## Структура

- `frontend/` — Next.js приложение (загрузка изображения, этапы AI-пайплайна, выбор станка, экспорт).
- `backend/` — FastAPI API с пайплайном обработки и промышленным `export/` модулем для станков.
- `.github/workflows/` — CI и автодеплой через GitHub Actions.

## Локальный запуск

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## GitHub Actions деплой (готово из коробки)

В репозитории уже есть workflows:
- `ci.yml` — запускает backend тесты.
- `deploy.yml` — публикует:
  - frontend в GitHub Pages,
  - backend Docker image в GHCR (`ghcr.io/<owner>/memorial-photo-pro-backend:latest`).

Остается только задать GitHub Repository Variable:
- `NEXT_PUBLIC_API_URL` — URL вашего backend (например, Render/Fly/VM с контейнером из GHCR).

После этого деплой срабатывает автоматически на `main` или вручную через `workflow_dispatch`.

## Основные endpoint'ы

- `POST /pipeline/enhance`
- `POST /pipeline/remove-bg`
- `POST /pipeline/outfit`
- `POST /pipeline/mockup`
- `POST /export/machine`

## Тесты

```bash
python -m pytest -q
```
