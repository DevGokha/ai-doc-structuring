# AI‑Powered Document Structuring & Data Extraction

Automatically convert an unstructured PDF into a well-structured Excel file. This project was built as part of the AI Intern — Document Structuring & Data Extraction assignment and provides both a CLI/Script interface and a Streamlit demo for interactive use.

Live demo: https://ai-doc-structuring-gjuvt4fsxe4mzbkqqxqueq.streamlit.app/

## Key features
- Extracts text from PDF pages using robust parsing (pdfplumber)
- Detects key:value pairs using rules and regular expressions
- Automatically detects logical sections / headings
- Merges multi-line and complex values into single cells
- Adds contextual comments for each key:value pair
- Preserves original wording (no summarization)
- Exports a clean Excel file with columns:
  - Section, Key, Value, Comments, Page, Raw Text

## Quick demo
1. Open the live demo link above
2. Upload `Data Input.pdf`
3. Click “Convert to Excel”
4. Download the generated `Output.xlsx`

## Requirements
- Python 3.8+
- See `requirements.txt` for pinned dependencies (pdfplumber, pandas, openpyxl, regex, streamlit, etc.)

## Install & Run (Local)
1. Create a virtual environment
   - macOS / Linux:
     python -m venv venv
     source venv/bin/activate
   - Windows (Powershell):
     python -m venv venv
     .\venv\Scripts\Activate.ps1

2. Install dependencies
   pip install -r requirements.txt

3. Run the extraction script (CLI)
   python src/main.py

4. Run the Streamlit app (interactive)
   streamlit run demo_app.py

## Folder structure
ai-doc-structuring/
├── src/
│   ├── pdf_parser.py     # PDF reading and page extraction
│   ├── extractor.py      # Key:value detection and sectioning logic
│   ├── exporter.py       # Excel export (openpyxl / pandas)
│   └── main.py           # CLI entrypoint / orchestration
├── demo_app.py           # Streamlit web app for manual use
├── requirements.txt
└── data/
    ├── Data Input.pdf           (optional / sample input)
    └── Expected Output.xlsx     (reference output)

## Deployment
- The app is deployed on Streamlit Cloud. Use the demo link above to access the web UI without setup.
- To deploy your own instance, connect this repository to Streamlit Cloud and set the run command to:
  streamlit run demo_app.py

## Deliverables
- Full source code
- README with usage instructions
- Streamlit live demo
- Example `Output.xlsx` generated from the provided PDF

## Author
Dev Gokha  
AI/ML Developer | MERN Stack | Data Analytics | Python

## License
(Include a license of your choice, e.g., MIT) — add `LICENSE` file if needed.
