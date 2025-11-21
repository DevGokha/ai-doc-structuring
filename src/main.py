from pdf_parser import extract_lines_from_pdf, extract_full_text
from extractor import (
    extract_structured_rows,
    add_context_comments,
    extract_entities_from_text,
)
from exporter import export_rows_to_excel


def main():
    pdf_path = "data/Data Input.pdf"
    output_path = "data/Output.xlsx"

    # 1) basic line-level capture (100% content)
    lines = extract_lines_from_pdf(pdf_path)
    base_rows = extract_structured_rows(lines)

    # 2) text-level smart extraction (logical key:value pairs)
    full_text = extract_full_text(pdf_path)
    entity_rows = extract_entities_from_text(full_text)

    # combine both
    all_rows = base_rows + entity_rows
    all_rows = add_context_comments(all_rows)

    export_rows_to_excel(all_rows, output_path)

    print("Structured extraction completed. File saved at:", output_path)


if __name__ == "__main__":
    main()
