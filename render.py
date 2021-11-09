import logging
from pathlib import Path
from typing import Any, Dict
from uuid import uuid4

from docxtpl import DocxTemplate

from config import RENDERED_DIR

logging.basicConfig()
logger = logging.getLogger("processing")
logger.setLevel(level=logging.INFO)


class Render:
    @classmethod
    def render_file(cls, file_path: str, context: Dict[str, Any]) -> Path:
        logger.info(f"Received context: {context}")

        doc = DocxTemplate(file_path)
        doc.render(context)

        file_path = cls.get_path(
            base_name=context.get("FullName") or context.get("CashDocumentNumber")
        )

        logger.info("Saving rendered file to: {path}".format(path=file_path))
        doc.save(file_path)
        return file_path

    @classmethod
    def get_path(cls, base_name: str = None) -> Path:
        if base_name is None:
            base_name = str(uuid4())
        path = Path(RENDERED_DIR / base_name.lower().replace(" ", "-"))
        path.mkdir(parents=True, exist_ok=True)
        return path.joinpath("rendered-agreement.docx")
