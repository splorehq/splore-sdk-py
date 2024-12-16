import os
from tusclient import client
from tusclient.storage import filestorage
from tusclient.uploader import Uploader

storage = filestorage.FileStorage('storage_file')
print(storage._db.all())
storage._db.truncate()
file_path = "./examples/large_file_test.pdf"
absolute_path = os.path.abspath(file_path)

# Ensure file exists and is valid
if not os.path.exists(absolute_path):
    raise FileNotFoundError(f"File not found: {absolute_path}")
if not os.path.isfile(absolute_path):
    raise ValueError(f"Expected a file, but found a directory: {absolute_path}")

# Upload using tusclient
tus_url = "https://tusd.search.splore.st/files/"
uploader = client.TusClient(tus_url)
try:
    metadata_for_extraction = {
                "baseId": "STEN2iQ1hEDkDiQwRpiNSuX90nH2GXd",
                "userId": "ABUS2blXtjKNI0VOtQdqA1m1qprHljs",
                "isDataFile": "true",
                "customExtractionEnabled": "true",
                "filename":"large_test_file_1.pdf",
                "s3FileName": "large_test_file_1.pdf"
            }
    uploader.uploader(file_path=absolute_path, store_url=True, url_storage=storage, metadata=metadata_for_extraction).upload()
    print("raw_ur", uploader.url)
    print("File uploaded successfully.")
    print(storage._db.all())
except Exception as e:
    print(f"Error during upload: {e}")
