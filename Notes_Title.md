# Python Script Documentation

This documentation provides an overview of a Python script designed to establish a connection to a SQL Server, retrieve and process data, and execute SSH commands. The script is broken down into several functions, each serving a specific purpose.

## Prerequisites

Before running the script, ensure that the following Python libraries are installed:

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

## Constants

The script uses several constants that must be configured before execution:

- `SERVER_NAME`: Name of the SQL Server.
- `DATABASE`: Name of the database.
- `UID`: User ID for SQL Server authentication.
- `PWD`: Password for SQL Server authentication.
- `BATCH_SIZE`: Number of records to process in a batch.
- `FILEMAN_IP`: IP address of the FileMan server.
- `FILEMAN_USER`: Username for FileMan authentication.
- `FILEMAN_PASSWORD`: Password for FileMan authentication.
- `VISTA_USERNAME`: Username for VistA authentication.
- `VISTA_PASSWORD`: Password for VistA authentication.
- `FILEMAN_SETTING_FILE_PATH`: Path to the Excel file containing FileMan settings.

## Functions

### `establish_connection()`

Establishes a connection to the SQL Server.

**Returns**: 
- `conn` - Connection object if successful, otherwise `None`.

### `get_max_value_from_db(conn)`

Retrieves the maximum value from the `SIGNATURE_DATE_TIME` column in the `Notes_Title` table.

**Parameters**:
- `conn` - SQL Server connection object.

**Returns**: 
- `max_value` - The maximum date in the format `MM/DD/YYYY HH:MM AM/PM`.

### `update_excel_with_max_value(file_path, max_value)`

Updates the Excel file with the maximum value retrieved from the database.

**Parameters**:
- `file_path` - Path to the Excel file.
- `max_value` - Maximum value to update in the Excel file.

**Returns**: 
- `df` - Updated DataFrame.

### `generate_fileman_string(df)`

Generates a string for the FileMan search based on the updated Excel file.

**Parameters**:
- `df` - DataFrame containing the Excel file data.

**Returns**: 
- `fileman_string` - String for FileMan search.

### `setup_ssh_connection(host, username, password, port=22)`

Sets up an SSH connection.

**Parameters**:
- `host` - IP address or hostname.
- `username` - SSH username.
- `password` - SSH password.
- `port` - SSH port (default is 22).

**Returns**: 
- `ssh` - SSH connection object.

### `truncate_string(value, max_length)`

Truncates a string to the specified maximum length.

**Parameters**:
- `value` - String to truncate.
- `max_length` - Maximum length of the string.

**Returns**: 
- Truncated string if it exceeds the maximum length, otherwise the original string.

### `extract_data()`

Main function to extract data by connecting to the database and performing SSH operations.

### `close_connection(conn)`

Closes the database connection.

**Parameters**:
- `conn` - SQL Server connection object.

### `parse_file(filename, conn)`

Parses a file and inserts data into the database.

**Parameters**:
- `filename` - Name of the file to parse.
- `conn` - SQL Server connection object.

### `insert_data_batch(conn, data_list, columns)`

Inserts data into the database in batches.

**Parameters**:
- `conn` - SQL Server connection object.
- `data_list` - List of data to insert.
- `columns` - List of column names.

### `main_function()`

Orchestrates the entire process, including data extraction, parsing, and insertion into the database.

## Execution

The script is designed to run indefinitely in a loop. If an error is encountered, the script will wait for a minute and then retry the operation.

**Usage**:
To execute the script, simply run it as the main module:
```python
if __name__ == "__main__":
    while True:
        try:
            main_function()
        except Exception as e:
            print(f"Error encountered: {e}. Retrying in 1 minute...")
            main_function()
