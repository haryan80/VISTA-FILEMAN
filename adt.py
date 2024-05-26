import os
import time
import warnings
import pyodbc
import pandas as pd
import numpy as np
from tqdm import tqdm
import paramiko
from datetime import datetime, timedelta
from dotenv import load_dotenv


load_dotenv()

warnings.filterwarnings('ignore')

# Constants
SERVER_NAME=os.getenv('SERVER_NAME')
DATABASE=os.getenv('DATABASE')
UID=os.getenv('UID')
PWD=os.getenv('PWD')
BATCH_SIZE=os.getenv('BATCH_SIZE')
FILEMAN_IP=os.getenv('FILEMAN_IP')
FILEMAN_USER=os.getenv('FILEMAN_USER')
FILEMAN_PASSWORD=os.getenv('FILEMAN_PASSWORD')
VISTA_USERNAME=os.getenv('VISTA_USERNAME')
VISTA_PASSWORD=os.getenv('VISTA_PASSWORD')


FILEMAN_SETTING_FILE_PATH="fileman_adt_conditions.xlsx"

def establish_connection():
    """Establish a connection to the SQL Server."""
    try:
        conn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};'
                              f'SERVER={SERVER_NAME};'
                              f'DATABASE={DATABASE}; UID={UID}; PWD={PWD};')
        print("Connection successful!")
        return conn
    except pyodbc.Error as e:
        print("Connection error:", e)
        return None

def get_max_value_from_db(conn):
    """Retrieve the maximum value from the NUMBER column in the PATIENT_MOVEMENT table."""
    sql_get = "SELECT MAX(NUMBER) FROM PATIENT_MOVEMENT;"
    cursor = conn.cursor()
    cursor.execute(sql_get)
    max_value = cursor.fetchone()[0]
    cursor.close()
    return max_value if max_value is not None else 0

def update_excel_with_max_value(file_path, max_value):
    """Update the Excel file with the maximum value retrieved from the database."""
    df = pd.read_excel(file_path, header=None)
    df.iloc[3, 0] = max_value
    return df

def generate_fileman_string(df):
    """Generate a string for the FileMan search based on the updated Excel file."""
    return ''.join(str(row[0]) + '\n' if not pd.isna(row[0]) else '\x0d' for _, row in df.iterrows())

def setup_ssh_connection(host, username, password, port=22):
    """Set up an SSH connection."""
    paramiko.util.log_to_file("patient_movement.log")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username=username, password=password, port=port)
    return ssh

def execute_steps_via_ssh(channel, steps):
    """Execute steps via SSH channel."""
    for step in steps:
        channel.send(step)
        while not channel.recv_ready():
            time.sleep(3)
        out = channel.recv(9999)
        print(out.decode('cp1256'))
        if 'invalid signon attempts.' in out.decode('cp1256') or 'Device/IP address is locked in' in out.decode('cp1256') or 'Do you really want to halt? YES//' in out.decode('cp1256') or 'Not a valid ACCESS CODE' in out.decode('cp1256') :
            print(f"Sorry, invalid signon attempts, i will retry after 5 min")
            time.sleep(300)
            extract_data() 
            
def extract_data():
    """Main function to extract data by connecting to the database and performing SSH operations."""
    conn = establish_connection()
    if not conn:
        return

    max_value = get_max_value_from_db(conn)
    conn.close()
    print(f"The maximum value in the column NUMBER is: {max_value}")
    
    fileman_search = update_excel_with_max_value(FILEMAN_SETTING_FILE_PATH, max_value)
    fileman = generate_fileman_string(fileman_search)
    
    steps = [
        '\x0d',
        VISTA_USERNAME,
        '\x0d',
        VISTA_PASSWORD,
        '\x0d',
        '\x0d',
        'Search File Entries\n',
        fileman
    ]

    ssh = setup_ssh_connection(FILEMAN_IP, FILEMAN_USER, FILEMAN_PASSWORD)
    channel = ssh.invoke_shell()

    if os.path.exists('output_Adt.txt'):
        os.remove('output_Adt.txt')
    
    execute_steps_via_ssh(channel, steps)

    prev_output = ""
    while True:
        out = channel.recv(9999).decode('cp1256')
        with open('output_Adt.txt', 'a') as f:
            f.write(out)
        
        combined_output = prev_output + out
        prev_output = out

        if "MATCHES FOUND" in combined_output:
            break

    print("Data extraction ended.")
    ssh.close()

def close_connection(conn):
    """Close the database connection."""
    if conn:
        conn.close()
        print("Connection closed.")

def parse_file(filename, conn):
    """Parse the file and insert data into the database."""
    total_number = 0
    data_list = []
    count = 0
    num_lines = sum(1 for line in open(filename))
    pbar = tqdm(total=num_lines)
    
    columns = [
        "MRN", "NUMBER", "DATE/TIME", "TRANSACTION", "TYPE OF MOVEMENT", "WARD LOCATION",
        "ROOM-BED", "ADMISSION/CHECK-IN MOVEMENT", "DISCHARGE/CHECK-OUT MOVEMENT",
        "FACILITY TREATING SPECIALTY", "UJOP CPRS ORDER", "WARD AT DISCHARGE",
        "MAS MOVEMENT TYPE", "ATTENDING PHYSICIAN", "DIAGNOSIS [SHORT]",
        "ADMITTING REGULATION", "SCHEDULED ADMISSION?"
    ]
    
    with open(filename) as file:
        parsed_data = {}
        for line in file:
            if ">>>>>><<<<<<" in line and "THEN PRINT" not in line and "FIRST PRINT" not in line:
                delimiter_index = line.find(">>>>>><<<<<<")
                pbar.update(1)
                if line[delimiter_index + 12:].strip() != "":
                    key = line[:delimiter_index].strip()
                    value = line[delimiter_index + 12:].strip()
                    if key == 'MRN' and len(value) == 10:
                        continue
                    parsed_data[key] = value
            elif line.startswith("End Text >>>>>>>>>>"):
                pbar.update(1)
                data_list.append(parsed_data)
                parsed_data = {}
                count += 1
                
                if count == BATCH_SIZE:
                    insert_data_batch(conn, data_list, columns)
                    total_number += count
                    count = 0
                    data_list.clear()
            else:
                pbar.update(1)
    
    if data_list:
        insert_data_batch(conn, data_list, columns)
        total_number += count
    
    print(f"Total records inserted: {total_number}")

def insert_data_batch(conn, data_list, columns):
    """Insert data into the database in batches."""
    df= pd.DataFrame(data_list,columns=columns)
    df['MRN'] = pd.to_numeric(df['MRN'],errors='coerce')
    df['MRN'].fillna(np.nan, inplace=True)
    df['NUMBER'] = pd.to_numeric(df['NUMBER'],errors='coerce')
    df['NUMBER'].fillna(np.nan, inplace=True)
    df['UJOP CPRS ORDER'] = pd.to_numeric(df['UJOP CPRS ORDER'],errors='coerce')
    df['UJOP CPRS ORDER'].fillna(np.nan, inplace=True)
    df['DATE/TIME'] = pd.to_datetime(df['DATE/TIME'],format='%m/%d/%Y %I:%M %p',errors='coerce')
    df['ADMISSION/CHECK-IN MOVEMENT'] = pd.to_datetime(df['ADMISSION/CHECK-IN MOVEMENT'],format='%m/%d/%Y %I:%M %p',errors='coerce')
    df['DISCHARGE/CHECK-OUT MOVEMENT'] = pd.to_datetime(df['DISCHARGE/CHECK-OUT MOVEMENT'],format='%m/%d/%Y %I:%M %p',errors='coerce')
    df['DATE/TIME'].fillna(np.nan, inplace=True)
    df['ADMISSION/CHECK-IN MOVEMENT'].fillna(np.nan, inplace=True)
    df['DISCHARGE/CHECK-OUT MOVEMENT'].fillna(np.nan, inplace=True)
    df = df.where(pd.notnull(df), None)
    df = df.replace({np.nan: None})
    data_list = [tuple(row) for row in df.to_numpy()]
    cursor = conn.cursor()
    cursor.fast_executemany = True
    sql_insert = """
    INSERT INTO PATIENT_MOVEMENT (
        MRN, NUMBER, DATE_TIME, [TRANSACTION], TYPE_OF_MOVEMENT, WARD_LOCATION, 
        ROOM_BED, ADMISSION_CHECK_IN_MOVEMENT, DISCHARGE_CHECK_OUT_MOVEMENT, 
        FACILITY_TREATING_SPECIALTY, UJOP_CPRS_ORDER, WARD_AT_DISCHARGE, 
        MAS_MOVEMENT_TYPE, ATTENDING_PHYSICIAN, DIAGNOSIS_SHORT, 
        ADMITTING_REGULATION, SCHEDULED_ADMISSION
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    cursor.executemany(sql_insert, data_list)
    conn.commit()
    cursor.close()

if __name__ == "__main__":
    while True:
        try:
            extract_data()
            conn = establish_connection()
            if conn:
                try:
                    parse_file('output_Adt.txt', conn)
                finally:
                    close_connection(conn)
            print("The End")
            print(f"Success! The next loop will start in 5 minutes...")
            time.sleep(300)
            
        except Exception as e:
            print(f"Error encountered: {e}. Retrying in 5 minutes...")
            if conn:
                close_connection(conn)
            time.sleep(300)  # Wait for 5 minutes before retrying
