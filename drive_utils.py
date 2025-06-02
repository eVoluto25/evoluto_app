from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

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
