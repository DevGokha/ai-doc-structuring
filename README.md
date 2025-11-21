AI-Powered Document Structuring & Data Extraction

This project automatically converts an unstructured PDF document into a structured Excel file.
It was developed as part of the AI Intern – Document Structuring & Data Extraction Assignment. 

🔍 Objective

The system extracts text from Data Input.pdf, detects key–value pairs, identifies logical sections, merges multi-line values, and generates a well-structured Output.xlsx similar to the provided Expected Output.xlsx.

🚀 Live Demo

Use the web app here:
👉 (https://ai-doc-structuring-gjuvt4fsxe4mzbkqqxqueq.streamlit.app/)

Upload the PDF → Click “Convert to Excel” → Download the structured file.

✨ Features

Extracts 100% content from the PDF

Identifies key:value pairs using rules + regex

Automatically detects sections/headings

Merges multi-line or complex values

Adds context/comments for each key:value

Preserves original wording without summarization

Outputs a clean Excel file with:

Section

Key

Value

Comments

Page

Raw Text

📦 Folder Structure
ai-doc-structuring/
│
├── src/
│   ├── pdf_parser.py
│   ├── extractor.py
│   ├── exporter.py
│   └── main.py
│
├── demo_app.py
├── requirements.txt
└── data/
    ├── Data Input.pdf           (optional)
    └── Expected Output.xlsx     (reference)

🛠 Technologies

Python

pdfplumber

pandas

openpyxl

regex

Streamlit (for live demo)

▶️ Run Locally
1. Create environment
python -m venv venv
venv\Scripts\activate

2. Install dependencies
pip install -r requirements.txt

3. Run the extraction script
python src/main.py

4. Run the Streamlit app
streamlit run demo_app.py

📤 Deployment

The app is deployed using Streamlit Cloud.
You can directly access the web interface from the link provided above.

📁 Deliverables Provided

Full source code

README with instructions

Streamlit live demo

Final Output.xlsx generated from the provided PDF

👤 Author

Dev Gokha
AI/ML Developer | MERN Stack | Data Analytics | Python
