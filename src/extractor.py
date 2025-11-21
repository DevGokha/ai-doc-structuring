import re

# ---------- basic helpers ----------

def is_section_heading(line: str) -> bool:
    # ALL CAPS and short
    if line.isupper() and len(line.split()) <= 6:
        return True

    # Ends with colon and short
    if line.endswith(":") and len(line.split()) <= 8:
        return True

    return False


def split_key_value(line: str):
    """Detect simple key : value style pairs on one line."""
    for sep in [":", "-", "="]:
        if sep in line:
            parts = line.split(sep, 1)
            key = parts[0].strip()
            value = parts[1].strip()

            # Key should not be a long sentence
            if 1 <= len(key.split()) <= 7:
                return key, value

    return None, None


# ---------- line-based extraction (what you already had, improved) ----------

def extract_structured_rows(lines):
    """
    Turn raw PDF lines into row dicts.
    Keeps 100% of content and merges multiline values after a key.
    """
    rows = []
    current_section = ""
    last_key_index = None  # index of last key:value row

    for item in lines:
        page = item["page"]
        line = item["line_text"]

        # Section heading?
        if is_section_heading(line):
            current_section = line.rstrip(":")
            rows.append({
                "Section": current_section,
                "Key": "",
                "Value": "",
                "Comments": "",
                "Page": page,
                "Raw_Line": line
            })
            last_key_index = None
            continue

        # Key : Value?
        key, value = split_key_value(line)

        if key is not None:
            # new key:value
            rows.append({
                "Section": current_section,
                "Key": key,
                "Value": value,
                "Comments": "",
                "Page": page,
                "Raw_Line": line
            })
            last_key_index = len(rows) - 1
        else:
            # continuation of previous value?
            if last_key_index is not None:
                rows[last_key_index]["Value"] += "\n" + line
                rows[last_key_index]["Raw_Line"] += " | " + line
            else:
                # plain line, keep as-is
                rows.append({
                    "Section": current_section,
                    "Key": "",
                    "Value": "",
                    "Comments": "",
                    "Page": page,
                    "Raw_Line": line
                })

    return rows


def add_context_comments(rows):
    """Add prev/next line as simple context for rows that have a Key."""
    for i, row in enumerate(rows):
        if row["Key"]:
            context_lines = []

            if i - 1 >= 0:
                context_lines.append(rows[i - 1]["Raw_Line"])
            if i + 1 < len(rows):
                context_lines.append(rows[i + 1]["Raw_Line"])

            row["Comments"] = " | ".join(context_lines)

    return rows


# ---------- text-level, regex-based entity extraction (accuracy boost) ----------

def extract_entities_from_text(text: str):
    """
    Extract logical key:value pairs from the full PDF text using regex.
    This is tailored to the Vijay Kumar profile PDF.
    """
    rows = []

    def add(section, key, value, span=None):
        comments = ""
        if span is not None:
            snippet = text[span[0]:span[1]]
            comments = snippet.strip()
        rows.append({
            "Section": section,
            "Key": key,
            "Value": value,
            "Comments": comments,
            "Page": 1,           # single-page PDF
            "Raw_Line": comments or value
        })

    # --- Personal Info ---

    # Name, DOB (natural), birthplace, age phrase
    m = re.search(
        r"([A-Z][a-z]+ [A-Z][a-z]+) was born on ([^,]+),in ([^,]+, ?[^,]+), making him ([^.]+)\.",
        text
    )
    if m:
        span = m.span()
        name, dob_text, birthplace, age_phrase = [g.strip() for g in m.groups()]
        add("Personal Info", "Name", name, span)
        add("Personal Info", "Birthdate (text)", dob_text, span)
        add("Personal Info", "Birthplace", birthplace, span)
        add("Personal Info", "Age phrase", age_phrase, span)

    # ISO-format birthdate
    m = re.search(r"birthdate is formatted as (\d{4}-\d{2}-\d{2})", text)
    if m:
        add("Personal Info", "Birthdate (ISO)", m.group(1).strip(), m.span())

    # Blood group
    m = re.search(r"his ([ABO][+-]) blood group", text)
    if m:
        add("Personal Info", "Blood group", m.group(1).strip(), m.span())

    # Citizenship
    m = re.search(r"As an ([A-Za-z ]+) national", text)
    if m:
        add("Personal Info", "Citizenship", m.group(1).strip(), m.span())

    # Address line at end
    m = re.search(r"Address:([^\n]+)", text)
    if m:
        address_value = m.group(1).strip()
        add("Personal Info", "Address", address_value, m.span())

    # --- Career / Employment ---

    # First job
    m = re.search(
        r"professional journey began on ([^,]+), when he joined his first company as a ([^,]+) with an annual salary of ([0-9,]+ INR)",
        text
    )
    if m:
        span = m.span()
        start_date, first_role, first_salary = [g.strip() for g in m.groups()]
        add("Career", "First job start date", start_date, span)
        add("Career", "First job role", first_role, span)
        add("Career", "First job salary", first_salary, span)

    # Current role
    m = re.search(
        r"current role at ([^,]+) beginning on ([^,]+), where he serves as a ([^,]+) earning ([0-9,]+ INR annually)",
        text
    )
    if m:
        span = m.span()
        company, start_date, role, salary = [g.strip() for g in m.groups()]
        add("Career", "Current company", company, span)
        add("Career", "Current role start date", start_date, span)
        add("Career", "Current role title", role, span)
        add("Career", "Current salary", salary, span)

    # Previous company
    m = re.search(
        r"he worked at ([^,]+) from ([^,]+) to ([0-9]{4})",
        text
    )
    if m:
        span = m.span()
        company, from_date, to_year = [g.strip() for g in m.groups()]
        add("Career", "Previous company", company, span)
        add("Career", "Previous role period", f"{from_date} to {to_year}", span)

    # Peak salary
    m = re.search(r"peak salary of ([0-9,]+ INR)", text)
    if m:
        add("Career", "Peak salary", m.group(1).strip(), m.span())

    # --- Education ---

    # High school
    m = re.search(
        r"high school education at ([^,]+, [^,]+), where he completed his 12th standard in (\d{4}), achieving an outstanding ([0-9.]+%) overall score",
        text
    )
    if m:
        span = m.span()
        school, year_12, percent = [g.strip() for g in m.groups()]
        add("Education", "High school name", school, span)
        add("Education", "12th completion year", year_12, span)
        add("Education", "12th percentage", percent, span)

    # B.Tech
    m = re.search(
        r"He pursued his B\.Tech in ([^,]+) at ([^,]+), graduating with honors in (\d{4}) with a CGPA of ([0-9.]+) on a 10-point scale",
        text
    )
    if m:
        span = m.span()
        branch, college, year, cgpa = [g.strip() for g in m.groups()]
        add("Education", "B.Tech specialization", branch, span)
        add("Education", "B.Tech college", college, span)
        add("Education", "B.Tech graduation year", year, span)
        add("Education", "B.Tech CGPA", cgpa, span)

    # M.Tech
    m = re.search(
        r"earned his M\.Tech in ([^,]+) in (\d{4}), achieving an exceptional CGPA of ([0-9.]+)",
        text
    )
    if m:
        span = m.span()
        branch, year, cgpa = [g.strip() for g in m.groups()]
        add("Education", "M.Tech specialization", branch, span)
        add("Education", "M.Tech graduation year", year, span)
        add("Education", "M.Tech CGPA", cgpa, span)

    # --- Certifications ---

    m = re.search(r"AWS Solutions Architect exam in (\d{4}) with a score of ([0-9]+) out of 1000", text)
    if m:
        span = m.span()
        year, score = [g.strip() for g in m.groups()]
        add("Certifications", "AWS Solutions Architect year", year, span)
        add("Certifications", "AWS Solutions Architect score", score, span)

    m = re.search(r"Azure Data Engineer certification in (\d{4}) with ([0-9]+) points", text)
    if m:
        span = m.span()
        year, score = [g.strip() for g in m.groups()]
        add("Certifications", "Azure Data Engineer year", year, span)
        add("Certifications", "Azure Data Engineer score", score, span)

    m = re.search(r"Project Management Professional\s+certification, obtained in (\d{4}), was achieved with an \"([^\"]+)\"", text)
    if m:
        span = m.span()
        year, rating = [g.strip() for g in m.groups()]
        add("Certifications", "PMP year", year, span)
        add("Certifications", "PMP rating", rating, span)

    m = re.search(r"SAFe\s+Agilist certification earned him an outstanding ([0-9]+%) score", text)
    if m:
        add("Certifications", "SAFe Agilist score", m.group(1).strip(), m.span())

    # --- Skills ---

    m = re.search(r"SQL expertise\s+at a perfect ([0-9]+ out of 10)", text)
    if m:
        add("Skills", "SQL rating", m.group(1).strip(), m.span())

    m = re.search(r"Python proficiency scores ([0-9]+ out of 10)", text)
    if m:
        add("Skills", "Python rating", m.group(1).strip(), m.span())

    m = re.search(r"machine learning capabilities\s+rate ([0-9]+ out of 10)", text)
    if m:
        add("Skills", "Machine learning rating", m.group(1).strip(), m.span())

    m = re.search(r"cloud platform expertise.*rates ([0-9]+ out of 10)", text)
    if m:
        add("Skills", "Cloud platforms rating", m.group(1).strip(), m.span())

    m = re.search(r"data visualization skills in Power BI and Tableau score ([0-9]+ out of 10)", text)
    if m:
        add("Skills", "Data visualization rating", m.group(1).strip(), m.span())

    return rows
