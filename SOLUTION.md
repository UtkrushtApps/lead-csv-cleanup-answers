# Solution Steps

1. Import the required standard library modules (`csv` for CSV handling and `os` for file existence checks). Optionally add typing imports for clarity (`List`, `Dict`, `Set`).

2. Implement a `read_and_clean_leads(input_filename)` function that opens `leads.csv` using `csv.DictReader` so columns can be accessed by name (`name`, `email`, `source`).

3. Inside `read_and_clean_leads`, initialize `total_input_rows` to 0, an empty list `cleaned_leads`, and an empty set `seen_emails` to track which normalized email addresses have been processed.

4. Loop over each row produced by `DictReader`. For every row, increment `total_input_rows` before any validation so that all data rows (including invalid or duplicate ones) are counted.

5. Extract the raw email with `row.get("email", "")`, handling `None` by converting it to an empty string. Normalize it by calling `.strip().lower()` to remove surrounding spaces and make it lowercase.

6. If the normalized email is an empty string, treat the row as invalid and `continue` to the next row without adding it to `cleaned_leads`.

7. If the normalized email is already present in the `seen_emails` set, treat the row as a duplicate and `continue`. Otherwise, add the normalized email to `seen_emails` and keep this row.

8. For rows that pass validation and de-duplication, build a cleaned lead dictionary using the original `name`, the normalized `email`, and the original `source` (e.g., `{ "name": name, "email": normalized_email, "source": source }`) and append it to `cleaned_leads`.

9. After the loop finishes, return a dictionary from `read_and_clean_leads` containing `total_input_rows` and the `cleaned_leads` list.

10. Implement `write_cleaned_csv(output_filename, cleaned_leads)` that opens `cleaned_leads.csv` for writing, defines the header `['name', 'email', 'source']`, writes the header using `csv.DictWriter.writeheader()`, and then iterates through `cleaned_leads` writing each row with `writer.writerow(...)`.

11. Implement `write_report(report_filename, total_input_rows, cleaned_leads)` that computes `cleaned_row_count = len(cleaned_leads)` and a set of unique sources from the cleaned leads, then writes three lines to `report.txt`:
- `Total input rows: X`
- `Rows in cleaned_leads.csv: Y`
- `Unique sources in cleaned data: Z`

12. In the `main()` function, set filenames: `input_filename = 'leads.csv'`, `cleaned_filename = 'cleaned_leads.csv'`, and `report_filename = 'report.txt'`. Use `os.path.exists` to check if `leads.csv` exists. If it does not, print a short message like `"leads.csv not found. No leads to process."` and return without raising an error.

13. If `leads.csv` exists, call `read_and_clean_leads(input_filename)` to obtain `total_input_rows` and `cleaned_leads`. Then call `write_cleaned_csv(cleaned_filename, cleaned_leads)` and `write_report(report_filename, total_input_rows, cleaned_leads)` to create or overwrite the output files.

14. After writing the files, compute the number of cleaned rows and the number of unique sources from `cleaned_leads`, and print summary lines to the console (for example, `Total input rows: ...`, `Rows in cleaned_leads.csv: ...`, and `Unique sources in cleaned data: ...`) so the script still reports information when run.

15. Add the standard Python entry point guard `if __name__ == '__main__': main()` at the bottom of `main.py` so the script can be executed directly and performs the complete read-clean-write-report workflow.

