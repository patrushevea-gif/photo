from __future__ import annotations

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import StreamingResponse

from app.core.mockup import apply_stone_mockup
from app.export import export_for_machine
from app.services.ai_bg_remove import remove_background
from app.services.ai_enhance import enhance_face
from app.services.ai_inpaint import inpaint_outfit
from app.utils.image_utils import image_to_bytes, read_image

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/pipeline/enhance")
async def pipeline_enhance(file: UploadFile = File(...)) -> StreamingResponse:
    image = read_image(await file.read())
    processed = enhance_face(image)
    return StreamingResponse(iter([image_to_bytes(processed, "PNG")]), media_type="image/png")


@router.post("/pipeline/remove-bg")
async def pipeline_remove_bg(file: UploadFile = File(...)) -> StreamingResponse:
    image = read_image(await file.read())
    processed = remove_background(image)
    return StreamingResponse(iter([image_to_bytes(processed, "PNG")]), media_type="image/png")


@router.post("/pipeline/outfit")
async def pipeline_outfit(
    file: UploadFile = File(...),
    prompt: str = Form("black business suit, tie, highly detailed"),
) -> StreamingResponse:
    image = read_image(await file.read())
    processed = inpaint_outfit(image, prompt)
    return StreamingResponse(iter([image_to_bytes(processed, "PNG")]), media_type="image/png")


@router.post("/pipeline/mockup")
async def pipeline_mockup(file: UploadFile = File(...), stone: str = Form("gabbro")) -> StreamingResponse:
    image = read_image(await file.read())
    processed = apply_stone_mockup(image, stone=stone)
    return StreamingResponse(iter([image_to_bytes(processed, "PNG")]), media_type="image/png")


@router.post("/export/machine")
async def export_machine(file: UploadFile = File(...), machine: str = Form(...), dpi: int = Form(90)) -> StreamingResponse:
    image = read_image(await file.read())
    try:
        data, ext, mime = export_for_machine(image, machine=machine.lower(), dpi=dpi)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    headers = {"Content-Disposition": f'attachment; filename="memorial_export.{ext}"'}
    return StreamingResponse(iter([data]), media_type=mime, headers=headers)
