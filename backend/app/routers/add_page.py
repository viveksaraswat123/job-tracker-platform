from fastapi import APIRouter
from fastapi.responses import FileResponse
from pathlib import Path

router = APIRouter()
frontend_path = Path(__file__).parent.parent.parent.parent / "frontend"

@router.get("/add")
def serve_add_page():
    return FileResponse(frontend_path / "add.html")
