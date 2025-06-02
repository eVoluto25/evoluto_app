from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2 import service_account
import io

def upload_file_to_drive(filename, folder_id):
    gauth = GoogleAuth()
    gauth.LoadServiceConfigSettings()
    gauth.LocalWebserverAuth()  # solo per debug, in produzione usa credenziali service
    drive = GoogleDrive(gauth)

    file_drive = drive.CreateFile({
        'title': filename,
        'parents': [{'id': folder_id}]
    })
    file_drive.SetContentFile(filename)
    file_drive.Upload()
    return file_drive['id']

def create_drive_subfolder(folder_name, parent_folder_id):
    gauth = GoogleAuth()
    gauth.LoadServiceConfigSettings()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)

    folder_metadata = {
        'title': folder_name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [{'id': parent_folder_id}]
    }
    folder = drive.CreateFile(folder_metadata)
    folder.Upload()
    return folder['id']

def get_pdfs_from_drive(folder_id):
    creds = service_account.Credentials.from_service_account_file(
        'credentials.json', scopes=['https://www.googleapis.com/auth/drive']
    )
    service = build('drive', 'v3', credentials=creds)

    query = f"'{folder_id}' in parents and mimeType='application/pdf' and trashed=false"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    items = results.get('files', [])

    pdfs = []
    for item in items:
        file_id = item['id']
        file_name = item['name']
        request = service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
        fh.seek(0)
        pdfs.append({'name': file_name, 'content': fh.read()})

    return pdfs

async def gestisci_upload_pdf(file):
    try:
        contents = await file.read()
        pdf_reader = PdfReader(io.BytesIO(contents))
        testo_pdf = "\n".join(page.extract_text() for page in pdf_reader.pages if page.extract_text())

        # Estrazione nome azienda via GPT o fallback
        azienda = estrai_nome_azienda(testo_pdf)  # o passalo manualmente
        if not azienda:
            return {"error": "Impossibile identificare il nome dell'azienda"}

        # Crea sottocartella su Drive e carica il file
        folder_id = create_drive_subfolder(azienda, DRIVE_PARENT_FOLDER_ID)
        upload_file_to_drive(contents, file.filename, folder_id)

        # Triggera analisi (modifica se diversa)
        results = processa_documenti([contents], azienda)

        return {"status": "ok", "azienda": azienda, "results": results}
    
    except Exception as e:
        return {"error": str(e)}
