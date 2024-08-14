### # Documentation for Data Extraction and Processing Script

#### ## Overview

This script is designed to extract patient movement data from a SQL Server database, process it, and insert it into another table. The script includes SSH operations to retrieve specific data based on criteria defined in an Excel file. The operations are automated and designed to handle errors, with retry mechanisms in place.

#### ## Key Components

### ### 1. Environment Variables

   - `SERVER_NAME`: The name of the SQL Server.
   - `DATABASE`: The database name.
   - `UID`: The User ID for SQL Server authentication.
   - `PWD`: The password for SQL Server authentication.
   - `BATCH_SIZE`: The size of data batches for insertion into the database.
   - `FILEMAN_IP`: IP address for SSH connection.
   - `FILEMAN_USER`: SSH username.
   - `FILEMAN_PASSWORD`: SSH password.
   - `VISTA_USERNAME`: Username for VISTA access.
   - `VISTA_PASSWORD`: Password for VISTA access.
   - `optimus_prime` and `optimus_random`: Used to initialize the `Optimus` class for data encoding.

### ### 2. Dependencies

   - `os`, `time`, `warnings`: Standard Python libraries.
   - `pyodbc`: For database connection.
   - `pandas`, `numpy`: For data manipulation.
   - `tqdm`: For progress bars.
   - `paramiko`: For SSH connection.
   - `datetime`, `timedelta`: For date manipulation.
   - `Optimus`: A custom class for encoding data.

### ### 3. Functions

   - `establish_connection()`: Connects to the SQL Server database and returns a connection object.
   - `get_max_value_from_db(conn)`: Retrieves the maximum value from the `NUMBER` column in the `VISTA_PATIENT_MOVEMENT` table.
   - `update_excel_with_max_value(file_path, max_value)`: Updates an Excel file with the maximum value retrieved from the database.
   - `generate_fileman_string(df)`: Generates a string for FileMan search based on the updated Excel file.
   - `setup_ssh_connection(host, username, password, port=22)`: Establishes an SSH connection to a remote server.
   - `safe_date_convert(x)`: Safely converts date strings to a specific format, returning `NaN` on failure.
   - `extract_data()`: The main function that coordinates data extraction from the database and remote server via SSH.
   - `close_connection(conn)`: Closes the database connection.
   - `parse_file(filename, conn)`: Parses a text file and inserts the data into the database in batches.
   - `insert_data_batch(conn, data_list, columns)`: Inserts a batch of data into the `VISTA_PATIENT_MOVEMENT` table.
   - `main_function()`: Handles the overall execution flow, including retries on failure.

### ### 4. Execution Flow

   - The script begins by establishing a connection to the SQL Server and retrieving the maximum value from a specific column.
   - It updates an Excel file with this maximum value and generates a string to be used in a FileMan search.
   - An SSH connection is established to a remote server, and the script interacts with the server to execute the search.
   - The retrieved data is parsed and inserted into the database in batches.
   - The script runs in a continuous loop, automatically retrying on failure and waiting for 10 minutes between iterations.

### ### 5. Error Handling

   - The script includes error handling and retry logic. If an error occurs during any part of the process, the script waits for a minute before retrying.
   - The main function is recursively called on failure, ensuring continuous operation.

### ### 6. Usage

   - Run the script in an environment where all dependencies are installed, and the necessary credentials are set.
   - The script will automatically continue running, extracting data and inserting it into the database in a loop.

#### ## Conclusion

This script is a robust solution for automated data extraction, processing, and insertion, with built-in error handling and retry mechanisms to ensure continuous operation. Make sure all environment variables are correctly set before executing the script.