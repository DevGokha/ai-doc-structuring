import os
import tempfile
import sys

import streamlit as st

# make sure Python can find the src/ modules
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(CURRENT_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.append(SRC_DIR)

from pdf_parser import extract_lines_from_pdf, extract_full_text
from extractor import (
    extract_structured_rows,
    add_context_comments,
    extract_entities_from_text,
)
from exporter import export_rows_to_excel


def process_pdf_bytes(pdf_bytes) -> str:
    """Save uploaded PDF, run extraction, return path to generated Excel."""
    # write temp PDF
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(pdf_bytes)
        tmp_path = tmp.name

    # 1) line-level extraction
    lines = extract_lines_from_pdf(tmp_path)
    base_rows = extract_structured_rows(lines)

    # 2) full-text entity extraction
    full_text = extract_full_text(tmp_path)
    entity_rows = extract_entities_from_text(full_text)

    all_rows = base_rows + entity_rows
    all_rows = add_context_comments(all_rows)

    out_path = tmp_path.replace(".pdf", ".xlsx")
    export_rows_to_excel(all_rows, out_path)

    return out_path


def main():
    st.title("AI-Powered Document Structuring & Data Extraction")

    st.write(
        "Upload a PDF like **Data Input.pdf** and get a structured Excel file "
        "with extracted key:value pairs and full content capture."
    )

    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

    if uploaded_file is not None:
        if st.button("Convert to Excel"):
            with st.spinner("Processing..."):
                out_path = process_pdf_bytes(uploaded_file.read())
            st.success("Done! Download your structured Excel output below.")

            with open(out_path, "rb") as f:
                st.download_button(
                    label="Download Output.xlsx",
                    data=f,
                    file_name="Output.xlsx",
                    mime=(
                        "application/"
                        "vnd.openxmlformats-officedocument."
                        "spreadsheetml.sheet"
                    ),
                )


if __name__ == "__main__":
    main()
