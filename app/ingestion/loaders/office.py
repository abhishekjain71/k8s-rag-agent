import os
import logfire

from unstructured.partition.pptx import partition_pptx
from unstructured.partition.docx import partition_docx


def parse_office(file_path: str):
    with logfire.span("Office Document parsing", filename=file_path):
        try:
            ext = os.path.splitext(file_path)[1].lower()

            if ext == ".pptx":
                elements = partition_pptx(filename=file_path)

            elif ext == ".docx":
                elements = partition_docx(filename=file_path)

            else:
                raise ValueError(f"Unsupported Office file: {ext}")

            full_text = "\n".join(
                str(element) for element in elements
            )

            logfire.info(
                f"Successfully parsed {len(full_text)} characters."
            )

            return full_text

        except Exception as e:
            logfire.error(f"Office parse failed: {e}")
            raise