import csv
import os
from typing import List, Dict, Set


def read_and_clean_leads(input_filename: str) -> Dict[str, object]:
    """Read leads from a CSV file, clean and de-duplicate them.

    Returns a dictionary containing:
      - total_input_rows: int
      - cleaned_leads: List[Dict[str, str]]
    """
    total_input_rows: int = 0
    cleaned_leads: List[Dict[str, str]] = []
    seen_emails: Set[str] = set()

    # Open the input CSV and read rows using DictReader so we can address
    # columns by name (name, email, source).
    with open(input_filename, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            # Count every data row, even if we later discard it as invalid
            # or as a duplicate.
            total_input_rows += 1

            # Get the raw email value, handle missing key or None safely.
            raw_email = row.get("email", "")
            if raw_email is None:
                raw_email = ""

            # Normalize the email: trim spaces and convert to lowercase.
            normalized_email = raw_email.strip().lower()

            # Skip rows where email is missing/empty/whitespace-only.
            if not normalized_email:
                continue

            # Skip duplicate emails; keep only the first occurrence.
            if normalized_email in seen_emails:
                continue

            seen_emails.add(normalized_email)

            # Preserve the original name and source (spec only requires
            # cleaning/normalizing email).
            name = row.get("name", "") or ""
            source = row.get("source", "") or ""

            cleaned_leads.append(
                {
                    "name": name,
                    "email": normalized_email,
                    "source": source,
                }
            )

    return {
        "total_input_rows": total_input_rows,
        "cleaned_leads": cleaned_leads,
    }


def write_cleaned_csv(output_filename: str, cleaned_leads: List[Dict[str, str]]) -> None:
    """Write the cleaned leads to cleaned_leads.csv with the required header."""
    fieldnames = ["name", "email", "source"]

    with open(output_filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for lead in cleaned_leads:
            writer.writerow({
                "name": lead.get("name", ""),
                "email": lead.get("email", ""),
                "source": lead.get("source", ""),
            })


def write_report(report_filename: str, total_input_rows: int, cleaned_leads: List[Dict[str, str]]) -> None:
    """Generate the required text report summarizing the processing."""
    cleaned_row_count = len(cleaned_leads)
    unique_sources = {lead.get("source", "") for lead in cleaned_leads}
    unique_source_count = len(unique_sources)

    with open(report_filename, "w", encoding="utf-8") as f:
        f.write(f"Total input rows: {total_input_rows}\n")
        f.write(f"Rows in cleaned_leads.csv: {cleaned_row_count}\n")
        f.write(f"Unique sources in cleaned data: {unique_source_count}\n")


def main() -> None:
    input_filename = "leads.csv"
    cleaned_filename = "cleaned_leads.csv"
    report_filename = "report.txt"

    # If leads.csv is missing, print a short message and exit without error.
    if not os.path.exists(input_filename):
        print("leads.csv not found. No leads to process.")
        return

    # Read and clean the leads from the input CSV.
    result = read_and_clean_leads(input_filename)
    total_input_rows = result["total_input_rows"]
    cleaned_leads: List[Dict[str, str]] = result["cleaned_leads"]

    # Write cleaned_leads.csv with normalized, de-duplicated leads.
    write_cleaned_csv(cleaned_filename, cleaned_leads)

    # Write report.txt with summary statistics.
    write_report(report_filename, total_input_rows, cleaned_leads)

    # Print at least one line to the console summarizing what happened.
    cleaned_row_count = len(cleaned_leads)
    unique_sources = {lead.get("source", "") for lead in cleaned_leads}

    print(f"Total input rows: {total_input_rows}")
    print(f"Rows in cleaned_leads.csv: {cleaned_row_count}")
    print(f"Unique sources in cleaned data: {len(unique_sources)}")


if __name__ == "__main__":
    main()
