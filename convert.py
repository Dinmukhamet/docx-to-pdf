import logging
from pathlib import Path
from subprocess import call

logging.basicConfig()
logger = logging.getLogger("converting")
logger.setLevel(level=logging.INFO)


class Convert:
    @classmethod
    def convert_file(cls, file_path: Path) -> Path:
        output_dir = file_path.parent

        logger.info("Running libreoffice to convert docx to pdf!")
        call(
            f"libreoffice --headless --convert-to pdf --outdir {output_dir} {file_path}",
            shell=True,
        )

        # logger.info(f"\nCode: {result.returncode}\nStdout: {result.stdout}\nStderr: {result.stderr}")
        return output_dir.joinpath(f"{file_path.stem}.pdf")
