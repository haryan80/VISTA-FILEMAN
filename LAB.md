# Documentation for Data Extraction Script

## Overview
This script is designed to extract, process, and insert laboratory data into a SQL Server database. The main functions include establishing a connection to the database, retrieving and processing data, and handling the output through an SSH connection. Below is a detailed breakdown of the code components.

## Dependencies
The script relies on the following Python libraries:
- `os`: For interacting with the operating system.
- `time`: For time-related operations.
- `warnings`: For controlling the display of warnings.
- `pyodbc`: For connecting to SQL Server.
- `pandas`: For data manipulation and analysis.
- `numpy`: For numerical operations.
- `tqdm`: For displaying progress bars.
- `paramiko`: For SSH connections.
- `datetime` and `timedelta`: For handling dates and times.
- `IPython.display.clear_output`: For clearing the output of the notebook (optional).

## Constants
The script starts with defining constants for the server, database, user credentials, and file paths that are used throughout the script.

```python
SERVER_NAME=""
DATABASE=""
UID=""
PWD=""
BATCH_SIZE=2000
FILEMAN_IP=""
FILEMAN_USER=""
FILEMAN_PASSWORD=""
VISTA_USERNAME=""
VISTA_PASSWORD=""
FILEMAN_SETTING_FILE_PATH="fileman_labs_conditions2.xlsx"
```

## Functions

### 1. `establish_connection()`
Establishes a connection to the SQL Server using the provided credentials.

```python
def establish_connection():
    """Establish a connection to the SQL Server."""
```

### 2. `get_max_value_from_db(conn)`
Retrieves the maximum value from the `DATE REPORT COMPLETED` column in the `LAB` table.

```python
def get_max_value_from_db(conn):
    """Retrieve the maximum value from the NUMBER column in the LAB table."""
```

### 3. `update_excel_with_max_value(file_path, max_value)`
Updates the specified Excel file with the maximum value retrieved from the database.

```python
def update_excel_with_max_value(file_path, max_value):
    """Update the Excel file with the maximum value retrieved from the database."""
```

### 4. `generate_fileman_string(df)`
Generates a string for the FileMan search based on the updated Excel file.

```python
def generate_fileman_string(df):
    """Generate a string for the FileMan search based on the updated Excel file."""
```

### 5. `setup_ssh_connection(host, username, password, port=22)`
Sets up an SSH connection to the specified host using `paramiko`.

```python
def setup_ssh_connection(host, username, password, port=22):
    """Set up an SSH connection."""
```

### 6. `truncate_string(value, max_length)`
Truncates a string to the specified maximum length.

```python
def truncate_string(value, max_length):
    """Truncate string to the specified maximum length."""
```

### 7. `extract_data()`
Main function to extract data by connecting to the database and performing SSH operations.

```python
def extract_data():
    """Main function to extract data by connecting to the database and performing SSH operations."""
```

### 8. `close_connection(conn)`
Closes the database connection.

```python
def close_connection(conn):
    """Close the database connection."""
```

### 9. `parse_file(filename, conn)`
Parses the file and inserts data into the database in batches.

```python
def parse_file(filename, conn):
    """Parse the file and insert data into the database."""
```

### 10. `insert_data_batch(conn, data_list, columns, batch_size, start_date, end_date)`
Inserts data into the database in batches to avoid overloading the server.

```python
def insert_data_batch(conn, data_list, columns, batch_size, start_date, end_date):
    """Insert data into the database in batches."""
```

### 11. `main_function()`
Handles the main workflow, including error handling and retries.

```python
def main_function():
    """Main function that handles data extraction and processing."""
```

## Execution
The script is designed to run continuously, with the `main_function()` being called in an infinite loop. It includes error handling to retry the operation after a 1-minute delay if an error occurs.

```python
if __name__ == "__main__":
    while True:
        try:
            main_function()
        except Exception as e:
            print(f"Error encountered: {e}. Retrying in 1 minutes...")
            main_function()
```

## Conclusion
This script automates the process of extracting, processing, and inserting laboratory data into a SQL Server database. It includes robust error handling and is designed to run continuously, ensuring that the database is kept up-to-date with the latest data.