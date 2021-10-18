import asyncio
import logging
from pathlib import Path

logging.basicConfig()
logger = logging.getLogger("converting")
logger.setLevel(level=logging.INFO)


class Convert:
    @classmethod
    async def convert_file(cls, file_path: Path) -> Path:
        output_dir = file_path.parent
        command = (
            f"libreoffice --headless --convert-to pdf --outdir {output_dir} {file_path}"
        )
        logger.info("Running libreoffice to convert docx to pdf!")
        await asyncio.create_subprocess_shell(
            cmd=command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )

        # logger.info(f"\nCode: {result.returncode}\nStdout: {result.stdout}\nStderr: {result.stderr}")
        return output_dir.joinpath(f"{file_path.stem}.pdf")
