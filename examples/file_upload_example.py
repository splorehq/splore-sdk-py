from splore_sdk.utils.file_uploader import FileUploader

uploader = FileUploader(tus_url="https://api.splore.st/files/")
upload_url = uploader.upload_file(
    file_path="./examples/large_file_test.pdf",
    metadata={
        "baseId": "STEN2iQ1hEDkDiQwRpiNSuX90nH2GXd",
        "userId": "ABUS2blXtjKNI0VOtQdqA1m1qprHljs",
    }
)
print("Upload URL:", upload_url)