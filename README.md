# Memorial Photo Pro — архитектура и стартовый код

Этот репозиторий содержит базовую серверную реализацию ключевого шага ТЗ: экспорта обработанного портрета в машиночитаемый формат под разные ритуальные станки.

## Предлагаемая архитектура платформы

- **Frontend (Next.js + Tailwind)**
  - Левая панель: AI-инструменты (`Enhance`, `Remove BG`, `Outfit`).
  - Центр: канвас с `Before/After`-слайдером.
  - Правая панель: материалы камня + экспорт.
  - Модалка выбора станка (`Sauno`, `Mirtels`, `Graphica`, `Almaz`, `Zubr`, `Laser-M`).

- **Backend API (FastAPI)**
  - `POST /upload` — загрузка изображения.
  - `POST /pipeline/restore-face` — CodeFormer/GFPGAN.
  - `POST /pipeline/remove-bg` — SAM/Rembg.
  - `POST /pipeline/outfit` — SD Inpainting.
  - `POST /pipeline/mockup` — наложение текстуры камня.
  - `POST /export/machine` — конвертация под станок (реализовано в модуле `backend/machine_export.py`).

- **Workers/Queues**
  - Долгие AI-операции выполняются в очереди (например, Celery + Redis).

- **Storage**
  - Оригинал, промежуточные и экспортируемые версии файлов (S3-совместимое хранилище).

## Реализовано в коде

Функция `prepare_for_machine(image, machine_type)` в `backend/machine_export.py` делает:
1. Resize к физическому размеру (по умолчанию 300×400 мм) с `dpi=90`.
2. Grayscale + автоуровни контраста.
3. Специальная логика по станку:
   - `Sauno`: 8-bit grayscale BMP.
   - `Almaz`: 1-bit BMP со `Stucki dithering`.
   - `Laser-M`: инверсия + BMP.
   - Дополнительно: `Mirtels`, `Graphica`, `Zubr`, `Bryullov`.
4. Возвращает байты файла, расширение и MIME-тип.

## Запуск тестов

```bash
python -m pytest -q
```
