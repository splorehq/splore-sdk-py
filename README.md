# Splore Python SDK

The Splore Python SDK simplifies the process of interacting with the Splore document processing platform. Use it to upload files, process documents, and retrieve extracted data with minimal setup.

---

## Features

- **File Upload**: Seamlessly upload documents to the processing backend.
- **Task Management**: Start, monitor, and manage extraction tasks.
- **Data Retrieval**: Fetch structured results after processing is completed.
- **Modular Design**: Easily integrate with storage backends like AWS S3.
- **Error Handling**: Get meaningful errors and retry capabilities.

---

## Installation

Install the SDK via pip:

```bash
pip install splore-sdk
```

Install the SDK via pip with (optional example dependecies):

```bash
pip install splore-sdk[examples]
```

---

## Quick Start

Here’s how you can use the SDK to process a file:

### Prerequisites
1. **API Key and Agent ID**: Obtain these from the Splore console.
2. **Python 3.7+**: Ensure Python is installed on your system.

### Code Example

```python
from time import sleep
from splore_sdk import SploreSDK
import tempfile
from examples.aws import download_from_s3

# Initialize the SDK
sdk = SploreSDK(api_key="YOUR_API_KEY", agent_id="YOUR_AGENT_ID")

# Download the file from AWS S3
with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
    s3_uri = "s3://bucket-name/path-to-file.pdf"
    download_from_s3(s3_uri, tmp_file.name)
    
    # Upload the file
    file_upload_response = sdk.extractions.upload_file(tmp_file.name)
    file_id = file_upload_response.get('file_id')
    if file_id is None:
        raise RuntimeError("File upload failed!")

    # Start the extraction process
    sdk.extractions.start(file_id=file_id)

    # Monitor extraction status
    while True:
        status = sdk.extractions.processing_status(file_id=file_id)
        if status.get("fileProcessingStatus") == "COMPLETED":
            break
        sleep(10)  # Wait before checking again

    # Retrieve extracted data
    extracted_data = sdk.extractions.extracted_response(file_id=file_id)
    print("Extracted Data:", extracted_data)
```

---

## Modules Overview

### `SploreSDK`
This is the main entry point for the SDK.

- **Initialization**:
  ```python
  sdk = SploreSDK(api_key="YOUR_API_KEY", agent_id="YOUR_AGENT_ID")
  ```
- Provides access to `extractions`.

### `ExtractionManager`
Manage file processing and data extraction.

- **Methods**:
  - `upload_file(file_path: str) -> dict`: Uploads a file and returns its metadata.
  - `start(file_id: str) -> None`: Starts the extraction process for the uploaded file.
  - `processing_status(file_id: str) -> dict`: Retrieves the current status of the processing task.
  - `extracted_response(file_id: str) -> dict`: Fetches the processed data.

### `AWS Integration`
Easily download files from AWS S3 using:
```python
from examples.aws import download_from_s3
download_from_s3(s3_uri, local_path)
```

---

## Advanced Usage

### Polling Interval Configuration
Customize the polling interval for task monitoring:
```python
while True:
    status = sdk.extractions.processing_status(file_id=file_id)
    if status.get("fileProcessingStatus") == "COMPLETED":
        break
    sleep(5)  # Set custom polling interval
```

### Error Handling
Handle errors gracefully:
```python
try:
    sdk.extractions.upload_file(file_path)
except FileUploadError as e:
    print("Error uploading file:", e)
```

---

## FAQ

### 1. How do I get an API Key?
- Sign up on the Splore console and navigate to the API section to generate a key.

### 2. Can I use this SDK asynchronously?
- Asynchronous support will be added in a future release.

### 3. Which file formats are supported?
- currently we are supporting PDF files only.

---

## Support

For questions or issues, please open a ticket on [GitHub Issues](https://github.com/splorehq/splore-sdk-py/issues) or email us at support@splore.com.

---

## License

This SDK is licensed under the MIT License. See [LICENSE](LICENSE) for details.
