import os
import tempfile
from typing import IO, List, Optional

from unstructured.documents.elements import Element
from unstructured.partition.common import convert_office_doc
from unstructured.partition.pptx import partition_pptx


def partition_ppt(
    filename: Optional[str] = None, file: Optional[IO] = None, include_page_breaks: bool = False
) -> List[Element]:
    """Partitions Microsoft PowerPoint Documents in .ppt format into their document elements.

    Parameters
    ----------
    filename
        A string defining the target filename path.
    file
        A file-like object using "rb" mode --> open(filename, "rb").
    include_page_breaks
        If True, includes a PageBreak element between slides
    """
    if not any([filename, file]):
        raise ValueError("One of filename or file must be specified.")

    if filename is not None and not file:
        _, filename_no_path = os.path.split(os.path.abspath(filename))
        base_filename, _ = os.path.splitext(filename_no_path)
    elif file is not None and not filename:
        tmp = tempfile.NamedTemporaryFile(delete=False)
        tmp.write(file.read())
        tmp.close()
        filename = tmp.name
        _, filename_no_path = os.path.split(os.path.abspath(tmp.name))
    else:
        raise ValueError("Only one of filename or file can be specified.")

    if not os.path.exists(filename):
        raise ValueError(f"The file {filename} does not exist.")

    base_filename, _ = os.path.splitext(filename_no_path)

    with tempfile.TemporaryDirectory() as tmpdir:
        convert_office_doc(filename, tmpdir, target_format="pptx")
        pptx_filename = os.path.join(tmpdir, f"{base_filename}.pptx")
        elements = partition_pptx(filename=pptx_filename, metadata_filename=filename)

    return elements
