# cis6930sp24 -- Assignment0 

## Name:
Vandit Arvind Shah  
UFID: 50341980

## Assignment Description
Assignment0 for the CIS6930 course involves creating a Python script to streamline the collection of incident summary data from the Norman Police Department's website. The script downloads incident PDFs, extracts relevant details, stores them in an SQLite database, and provides summary information. The project includes comprehensive unit tests and documentation to ensure code quality.

## How to install
## How to Install 
1. Clone repository to your local machine:
```sh
$ git clone https://github.com/ShahVandit/cis6930sp24-assignment0
$ cd cis6930sp24-assignment0
```
2. Using Pipenc and Installing prerequisites:
   $ pipenv install
3. Verify installation:
   $ pipenv --version
4. Installing the dependencies
   $ pipenv install requests PyPDF

## How to run
To process incident reports, use the following commands:
- For a specific incident report:  
  `pipenv run python main.py --incidents <url>`
- Example usage with a provided URL:  
  `pipenv run python main.py --incidents "https://www.normanok.gov/sites/default/files/documents/2024-01/2024-01-01_daily_incident_summary.pdf"`

## Functions Overview
### `main.py`
This script encapsulates the core functionality:
- **fetchincidents(url):**  
  Fetches URLs of PDF incident reports from the provided webpage.

- **extractincidents(pdf_url):**  
  Extracts incident data from a given PDF URL, downloading the file and parsing the content to gather incident details.

- **createdb():**  
  Creates or opens an SQLite database and prepares a table for storing incident data.

- **populatedb(db, incidents):**  
  Inserts parsed incident data into the SQLite database.

- **status(db):**  
  Prints a summary of incidents by nature, including counts for each category.

- **main(url):**  
  Orchestrates the process of fetching PDF URLs, extracting incident data, storing it in a database, and displaying a summary.

## Database Development (`normandb`)
The SQLite database, `normandb`, contains a table `incidents` with the schema:
- `incident_time TEXT`
- `incident_number TEXT`
- `incident_location TEXT`
- `nature TEXT`
- `incident_ori TEXT`

## Known Issues
- **SQL Injection Vulnerability:**  
  The current implementation may be prone to SQL injection. Parameterized queries are recommended to mitigate this risk.

- **PDF Parsing Limitations:**  
  The extraction logic depends heavily on the PDF's layout and formatting. Changes in the document structure could impair data extraction.

- **Incomplete Nature Field Handling:**  
  The logic assumes empty `nature` fields are represented as empty strings, which may not always be accurate.

## Assumptions
- **PDF Structure Consistency:**  
  Assumes the incident PDFs maintain a consistent format and structure.

- **SQLite Suitability:**  
  Assumes SQLite meets all requirements for data storage in this context.

- **Reliable Network Access:**  
  Assumes stable internet access for downloading PDFs.

- **Accurate PDF Text Extraction:**  
  Assumes the extraction of text from PDFs is accurate and complete.

## Test Cases
### `functionality_test.py`
Implements unit tests to validate data extraction accuracy from PDFs:
- **test_extract_data_from_pdf(pdf_url, expected_count):**  
  Tests whether the `extractincidents` function accurately extracts the expected number of incidents from specific PDF URLs.

## Running Tests
To run the test cases, use the following command:
```bash
pytest functionality_test.py
