import os
import pyzipper
import pandas as pd
import hashlib
import chardet

source_directory = r"D:\Workspace\zipped-files"
destination_directory = r"D:\Workspace\unzipped-files"

def unzip_files(source_directory, destination_directory, password):
    os.makedirs(destination_directory, exist_ok=True)

    processed_files = 0
    for filename in os.listdir(source_directory):
        if filename.endswith(".zip"):
            zip_path = os.path.join(source_directory, filename)
            try:
                with pyzipper.AESZipFile(zip_path, 'r') as zf:
                    zf.setpassword(password)
                    zf.extractall(destination_directory)
                    processed_files += 1
                    print(f"Extracted: {filename}")
            except Exception as e:
                print(f"Failed to extract {filename}: {e}")

    print(f"Total files extracted: {processed_files}")
    return processed_files

def get_file_metrics(destination_directory):
    log_file_path = os.path.join(destination_directory, "csv_log.txt")
    with open(log_file_path, "w") as log_file:
        log_file.write("Filename,File Size (Bytes),Number of Records,Number of Columns,Encoding,Checksum (SHA256)\n")
        processed_files = 0

        for filename in os.listdir(destination_directory):
            if filename.endswith(".csv"):
                file_path = os.path.join(destination_directory, filename)
                file_size = os.path.getsize(file_path)

                num_records = "N/A"
                num_columns = "N/A"
                encoding = "N/A"
                checksum = "N/A"

                try:
                    with open(file_path, 'rb') as f:
                        raw_data = f.read(10000)
                        encoding = chardet.detect(raw_data)['encoding']

                    with open(file_path, 'rb') as f:
                        checksum = hashlib.sha256(f.read()).hexdigest()

                    chunk_iter = pd.read_csv(file_path, chunksize=1000, encoding=encoding)
                    num_records = sum(len(chunk) for chunk in chunk_iter)

                    num_columns = len(pd.read_csv(file_path, nrows=0, encoding=encoding).columns)
                except pd.errors.EmptyDataError:
                    num_records = "Empty File"
                except Exception as e:
                    num_records = f"Error: {e}"

                log_file.write(f"{filename},{file_size},{num_records},{num_columns},{encoding},{checksum}\n")
                processed_files += 1

                print(f"Processed: {filename} | Size: {file_size} bytes | Records: {num_records} | Columns: {num_columns} | Encoding: {encoding} | Checksum: {checksum}")

    print(f"Log file created at: {log_file_path}")
    return processed_files

if __name__ == "__main__":
    password = input("Enter the zip file password: ").encode()
    if (len(password) == 0):
        print("No password provided. Proceeding with no password.")
        password = None

    extracted = unzip_files(source_directory, destination_directory, password)
    processed = get_file_metrics(destination_directory)

    print(f"Extraction complete. {extracted} zip files processed.")
    print(f"CSV metrics logged for {processed} files.")