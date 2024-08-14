# Documentation for Python Code

This document provides an overview of the provided Python script, explaining its purpose, functionality, and usage. The script connects to a SQL Server database, retrieves data, processes it, and interacts with a remote server via SSH to extract patient visit information. Below is a detailed breakdown of the key components and functions.

## Dependencies

The following Python libraries are required for this script:
- `os`
- `time`
- `warnings`
- `pyodbc`
- `pandas`
- `numpy`
- `tqdm`
- `paramiko`
- `datetime`
- `IPython.display`

## Constants

- `FILEMAN_SETTING_FILE_PATH`: Path to the Excel file containing FileMan visit conditions.
- `my_optimus`: Instance of the `Optimus` class for encoding MRN numbers.

## Functions

### `establish_connection()`
Establishes a connection to the SQL Server database.

- **Returns**: A connection object if successful, `None` if the connection fails.

### `get_max_value_from_db(conn)`
Retrieves the maximum value from the `NUMBER` column in the `VISTA_VISIT` table.

- **Parameters**: 
  - `conn`: The database connection object.
- **Returns**: The maximum value from the `NUMBER` column.

### `update_excel_with_max_value(file_path, max_value)`
Updates the Excel file with the maximum value retrieved from the database.

- **Parameters**:
  - `file_path`: Path to the Excel file.
  - `max_value`: The maximum value retrieved from the database.
- **Returns**: Updated DataFrame.

### `generate_fileman_string(df)`
Generates a string for the FileMan search based on the updated Excel file.

- **Parameters**:
  - `df`: DataFrame containing the Excel data.
- **Returns**: A formatted string for FileMan search.

### `setup_ssh_connection(host, username, password, port=22)`
Sets up an SSH connection to the remote server.

- **Parameters**:
  - `host`: SSH server hostname or IP address.
  - `username`: SSH username.
  - `password`: SSH password.
  - `port`: SSH port number (default is 22).
- **Returns**: An SSH client object.

### `safe_date_convert(x)`
Safely converts a date to the format `YYYY-MM-DD HH:MM AM/PM`.

- **Parameters**:
  - `x`: The date to be converted.
- **Returns**: Formatted date string or `NaN` if conversion fails.

### `extract_data()`
Main function that extracts data by connecting to the database and performing SSH operations.

- **Procedure**:
  - Establishes a connection to the database.
  - Retrieves the maximum value from the `VISTA_VISIT` table.
  - Updates the Excel file with the maximum value.
  - Generates a FileMan search string.
  - Sets up an SSH connection and sends commands to the remote server.
  - Receives and processes the output from the remote server.
  
### `close_connection(conn)`
Closes the database connection.

- **Parameters**:
  - `conn`: The database connection object.

### `parse_file(filename, conn)`
Parses the file and inserts data into the database.

- **Parameters**:
  - `filename`: The name of the file to be parsed.
  - `conn`: The database connection object.

### `insert_data_batch(conn, data_list, columns)`
Inserts data into the database in batches.

- **Parameters**:
  - `conn`: The database connection object.
  - `data_list`: List of data to be inserted.
  - `columns`: List of column names.

### `main_function()`
Main function that orchestrates the data extraction and processing workflow.

- **Procedure**:
  - Calls `extract_data()` and `parse_file()` in a loop.
  - Handles exceptions and retries operations after a delay.

## Usage

The script is intended to run in a loop, continuously extracting and processing data. It handles errors gracefully by retrying the operations after a delay.

To run the script, execute the following command:
```python
python script_name.py
```

## Error Handling

- If an error occurs during database connection, SSH connection, or data parsing, the script will print an error message and retry the operation after a delay.

## Conclusion

This script automates the extraction and processing of patient visit data from a remote server. It is designed to be robust, with error handling and retries to ensure smooth operation in case of network or database issues.