import pandas as pd

def export_lines_to_excel(lines, output_path: str):
    df = pd.DataFrame(lines)
    df.to_excel(output_path, index=False)

def export_rows_to_excel(rows, output_path: str):
    df = pd.DataFrame(rows)
    df.to_excel(output_path, index=False)
