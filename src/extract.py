import os
import csv
import json
import fitz
from docx import Document
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload

input_folder = 'resumes'
out_folder = 'data'
csv_file = 'resume_data.csv'
json_file = 'resume_data.json'
credentials_path = 'credentials.json'
folder_id = '1eKS364a-vSlMFtmdA0EJYOGHGUS5W6jHTIaixBE6lfn6wHyBw5inWw_My3-Nl5G4nCXbB5T6'

os.makedirs(input_folder, exist_ok=True)
os.makedirs(out_folder, exist_ok=True)
csv_path = os.path.join(out_folder, csv_file)
json_path = os.path.join(out_folder, json_file)
open(csv_path, 'w').close()
open(json_path, 'w').close()

def authenticate_drive(credentials_path):
    """Authenticate and return the Google Drive API service."""
    creds = service_account.Credentials.from_service_account_file(credentials_path, scopes=['https://www.googleapis.com/auth/drive'])
    return build('drive', 'v3', credentials=creds)

def list_files_in_folder(drive_service, folder_id):
    """List all files in the specified folder."""
    page_token = None
    files = []

    while True:
        response = drive_service.files().list(
            q=f"'{folder_id}' in parents",
            fields="nextPageToken, files(id, name)",
            pageToken=page_token
        ).execute()

        files.extend(response.get('files', []))
        page_token = response.get('nextPageToken', None)

        if not page_token:
            break

    return files

def extract_person_name(raw_base):
    """Extract and format the person's name."""
    name_parts = raw_base.split("-")
    google_name = name_parts[-1].strip()
    return google_name.replace(" ", "_").lower()

def read_pdf_content(file_path):
    """Read content from a PDF file."""
    doc = fitz.open(file_path)
    text = ''
    for page_num in range(doc.page_count):
        page = doc[page_num]
        text += page.get_text()
    return text

def read_docx_content(file_path):
    """Read content from a DOCX file."""
    doc = Document(file_path)
    paragraphs = [paragraph.text for paragraph in doc.paragraphs]
    return '\n'.join(paragraphs)

def append_to_csv(csv_path, name, json_data):
    """Append data to a CSV file."""
    with open(csv_path, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['file', 'resume_data']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # If the file is empty, write the header
        if csvfile.tell() == 0:
            writer.writeheader()

        writer.writerow({'file': name, 'resume_data': json_data})

def main():
    drive_service = authenticate_drive(credentials_path) # Authenticate Google Drive
    
    files = list_files_in_folder(drive_service, folder_id)
    print(f"Total files in the folder: {len(files)}")
    
    data = {}
    
    for file in files:
        file_id = file['id']
        file_name = file['name']
        
        base, extension = os.path.splitext(file_name)
        cleaned_name = extract_person_name(base)
        download_path = os.path.join(input_folder, f"{cleaned_name}{extension}".lower())
        
        try:
            request = drive_service.files().get_media(fileId=file_id)
            with open(download_path, 'wb') as fh:
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while not done:
                    status, done = downloader.next_chunk()
            print(f"Downloaded - File Name: {file_name}, File ID: {file_id}, Exported To: {download_path}")
            
            # Reading the content based on the file type
            if extension.lower() == '.pdf':
                text = read_pdf_content(download_path)
            elif extension.lower() in ['.doc', '.docx']:
                text = read_docx_content(download_path)
            else:
                continue  # Skip unsupported file types
            
        except Exception as e:
            print(f"Error processing {file_name}: {e}")
            text = "Error - No data retrieved" # f"Error - {str(e)}"
        
        # Adding to the dictionary and CSV file
        data[cleaned_name] = text
        json_data = json.dumps({'payload': text})
        append_to_csv(csv_path, cleaned_name, json_data)

    print("Processing completed.")
    
    # Writing to JSON file
    with open(json_path, 'w') as file:
        json.dump(data, file, indent=4)

    print(f"Data has been written to {json_path}")


if __name__ == "__main__":
    main()

