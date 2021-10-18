from pathlib import Path
from typing import Any, Dict

import aiofiles
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel

import config
from convert import Convert
from render import Render

app = FastAPI()


class Data(BaseModel):
    file_path: str
    content: Dict[str, Any]


@app.post("/upload-template")
async def upload_template(file: UploadFile = File(...)):
    file_path = Path(config.TEMPLATES_DIR / file.filename)
    async with aiofiles.open(file_path, "wb") as out_file:
        content = await file.read()
        await out_file.write(content)
    return {"filename": file_path}


@app.post("/download-converted", response_class=FileResponse)
async def download_converted(data: Data):
    rendered_file: Path = Render.render_file(data.file_path, data.content)
    converted_file: Path = await Convert.convert_file(rendered_file)
    if not converted_file.exists():
        raise HTTPException(status_code=500, detail="Failed to convert file.")
    return converted_file
