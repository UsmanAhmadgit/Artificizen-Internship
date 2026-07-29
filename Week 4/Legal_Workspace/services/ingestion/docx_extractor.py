import io
import docx
from services.ingestion.ocr_utils import extract_text_from_image

def extract_docx_chunks(file_bytes: bytes) -> list[str]:
    if not file_bytes or len(file_bytes) == 0:
        return []

    try:
        doc = docx.Document(io.BytesIO(file_bytes))
        elements = []
        current_heading = "General"

        for child in doc.element.body:
            if child.tag.endswith('p'):
                para = docx.text.paragraph.Paragraph(child, doc)
                text = para.text.strip()
                if not text:
                    continue
                if para.style and para.style.name and para.style.name.startswith('Heading'):
                    current_heading = text
                    elements.append(f"## Section: {text}")
                else:
                    elements.append(f"[{current_heading}] {text}")

            elif child.tag.endswith('tbl'):
                table = docx.table.Table(child, doc)
                table_rows = []
                headers = []

                for i, row in enumerate(table.rows):
                    row_cells = [cell.text.strip().replace('\n', ' ') for cell in row.cells if cell.text]
                    if not any(row_cells):
                        continue

                    if i == 0:
                        headers = row_cells
                        header_str = " | ".join(headers)
                        table_rows.append(f"[{current_heading} - Table Header] {header_str}")
                    else:
                        if headers and len(headers) == len(row_cells):
                            row_str = " | ".join([f"{h}: {v}" if h else v for h, v in zip(headers, row_cells)])
                        else:
                            row_str = " | ".join(row_cells)
                        table_rows.append(f"[{current_heading} - Table Row] {row_str}")

                if table_rows:
                    elements.extend(table_rows)

        if hasattr(doc, 'inline_shapes'):
            for shape in doc.inline_shapes:
                try:
                    if shape.type == docx.enum.shape.WD_INLINE_SHAPE.PICTURE:
                        image_bytes = getattr(shape.image, 'blob', None) or getattr(shape, 'blob', None)
                        if image_bytes:
                            img_text = extract_text_from_image(image_bytes)
                            if img_text.strip():
                                elements.append(f"[{current_heading} - Image OCR]: {img_text.strip()}")
                except Exception as img_err:
                    print(f"Skipping unreadable docx image: {img_err}")
                    continue

        if not elements:
            return []

        chunks = []
        current_chunk = []
        current_len = 0

        for item in elements:
            if current_len + len(item) > 800 and current_chunk:
                chunks.append("\n\n".join(current_chunk))
                
                last_item = current_chunk[-1]
                current_chunk = [last_item, item]
                current_len = len(last_item) + len(item)
            else:
                current_chunk.append(item)
                current_len += len(item)

        if current_chunk:
            chunks.append("\n\n".join(current_chunk))

        return chunks

    except Exception as e:
        raise RuntimeError(f"Failed to parse DOCX document: {str(e)}")