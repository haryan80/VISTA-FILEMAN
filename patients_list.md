### Python Code Documentation

#### Overview
This script is designed to perform the extraction and processing of patient data from a SQL Server database, update an Excel file, generate a search string for FileMan, and handle data insertion into the database. It includes operations for establishing database and SSH connections, data parsing, and error handling. 

The script follows these key steps:

1. **Establish Database Connection**: Connect to the SQL Server database.
2. **Fetch Data**: Retrieve the most recent data based on specific date columns.
3. **Update Excel File**: Modify an Excel file with the fetched data.
4. **SSH Connection and Data Retrieval**: Generate a search string for FileMan, execute it over SSH, and fetch the results.
5. **Data Parsing and Insertion**: Parse the fetched data and insert it into the SQL Server database.
6. **Looping Mechanism**: The script is designed to run continuously, with error handling and retry mechanisms in place.

#### Dependencies
The following Python packages are required:
- `os`
- `time`
- `warnings`
- `pyodbc`
- `pandas`
- `numpy`
- `tqdm`
- `paramiko`
- `datetime`
- `IPython`

#### Constants
- **Database Connection Parameters**: `SERVER_NAME`, `DATABASE`, `UID`, `PWD`
- **Batch Processing**: `BATCH_SIZE`
- **SSH Connection Parameters**: `FILEMAN_IP`, `FILEMAN_USER`, `FILEMAN_PASSWORD`
- **Excel File Path**: `FILEMAN_SETTING_FILE_PATH`
- **Optimus Instance**: `optimus_prime`, `optimus_random`

#### Functions

- **`establish_connection()`**:  
  Establishes a connection to the SQL Server.

- **`get_max_value_from_db(conn)`**:  
  Retrieves the latest date from the `DATE_OF_LAST_UPDATE` or `DATE_OF_DEATH` columns in the `VISTA_PATIENTS` table.

- **`update_excel_with_max_value(file_path, max_value)`**:  
  Updates the specified Excel file with the maximum date value retrieved from the database.

- **`generate_fileman_string(df)`**:  
  Generates a search string for FileMan based on the updated Excel file.

- **`setup_ssh_connection(host, username, password, port=22)`**:  
  Establishes an SSH connection to the specified host.

- **`truncate_string(value, max_length)`**:  
  Truncates a string to the specified maximum length.

- **`extract_data()`**:  
  Main function that extracts data by connecting to the database and performing SSH operations.

- **`close_connection(conn)`**:  
  Closes the database connection.

- **`parse_file(filename, conn)`**:  
  Parses the output file and prepares data for insertion into the database.

- **`insert_data_(conn, data_list, columns)`**:  
  Inserts parsed data into the SQL Server database in batches.

- **`main_function()`**:  
  Orchestrates the entire data extraction, processing, and insertion workflow. It includes error handling and retries if any operation fails.

#### Usage
The script is designed to run continuously. When executed, it will repeatedly perform the following:
1. Establish a connection to the database.
2. Extract and update data.
3. Generate a search string for FileMan and perform the search via SSH.
4. Parse the resulting data and insert it into the database.
5. Handle any errors by retrying after a delay.

To execute the script:
```python
if __name__ == "__main__":
    while True:
        try:
            main_function()
        except Exception as e:
            print(f"Error encountered: {e}. Retrying in 10 minutes...")
            time.sleep(600)
            main_function()
```

This structure ensures that the script runs robustly and handles any interruptions or errors by retrying operations, making it suitable for long-running data extraction tasks.