# ADT Data Extraction and Processing Script

This Python script automates the extraction of patient movement data from a SQL Server database and processes it for further analysis. It is designed to connect to the database, retrieve the latest data, parse it, and insert it into the database.

## Features

- Establishes a connection to a SQL Server database using PyODBC.
- Retrieves the maximum value from a specific column in the database.
- Updates an Excel file with the maximum value retrieved from the database.
- Generates a search string for FileMan based on the updated Excel file.
- Sets up an SSH connection to a remote server using Paramiko.
- Executes steps via SSH channel and extracts data.
- Parses a text file containing patient movement data and inserts it into the database in batches.
- Handles errors gracefully and retries operations after a delay.

## Dependencies
- Python 3.10
- bcrypt==4.1.3
- cffi==1.16.0
- colorama==0.4.6
- cryptography==42.0.7
- et-xmlfile==1.1.0
- numpy==1.26.4
- openpyxl==3.1.2
- pandas==2.2.2
- paramiko==3.4.0
- pycparser==2.22
- PyNaCl==1.5.0
- pyodbc==5.1.0
- python-dateutil==2.9.0.post0
- python-dotenv==1.0.1
- pytz==2024.1
- six==1.16.0
- tqdm==4.66.4
- tzdata==2024.1

## Configuration

Before running the script, ensure you have set up the required environment variables in a `.env` file:
SERVER_NAME=
DATABASE=
UID=
PWD=
BATCH_SIZE=
FILEMAN_IP=
FILEMAN_USER=
FILEMAN_PASSWORD=
VISTA_USERNAME=
VISTA_PASSWORD=

## Usage

1. Install the required dependencies using `pip install -r requirements.txt`.
2. Set up the necessary environment variables in a `.env` file.
3. Run the script using `python adt.py`.

## License

Feel free to customize this template according to your project's specific details and requirements. Once you've created the README file, save it in the same directory as your `adt.py` script.

