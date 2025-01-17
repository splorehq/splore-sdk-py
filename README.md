# Splore Python SDK

The Splore Python SDK simplifies the process of interacting with the Splore document processing platform. Use it to upload files, process documents, and retrieve extracted data with minimal setup.

---

## Features

- **File Upload**: Seamlessly upload documents to the processing backend.
- **Task Management**: Start, monitor, and manage extraction tasks.
- **Data Retrieval**: Fetch structured results after processing is completed.
- **Modular Design**: Easily integrate with storage backends like AWS S3.
- **Error Handling**: Get meaningful errors and retry capabilities.
- **Agent Management**: Manage agents, including creation, updates, retrieval, and deletion.

---

## Installation

Install the SDK via pip:

```bash
pip install splore-sdk
```

Install the SDK via pip with (optional example dependencies):

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
sdk = SploreSDK(api_key="YOUR_API_KEY", base_id="YOUR_BASE_ID")

# Download the file from AWS S3
with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
    s3_uri = "s3://bucket-name/path-to-file.pdf"
    download_from_s3(s3_uri, tmp_file.name)

    # fetch agents related to your base
    agents = sdk.get_agents()

    agent_id1 = agents[0]["id"] # adjust according to your response and agent you want to select
    agent_id2 = agents[1]["id"]
    extraction_agent = sdk.init_agent(agent_id = agent_id1)
    chat_agent = sdk.init_agent(agent_id = agent_id2)

    # Upload the file
    file_upload_response = extraction_agent.extractions.upload_file(tmp_file.name)
    file_id = file_upload_response.get('file_id')
    if file_id is None:
        raise RuntimeError("File upload failed!")

    # Start the extraction process
    extraction_agent.extractions.start(file_id=file_id)

    # Monitor extraction status
    while True:
        status = extraction_agent.extractions.processing_status(file_id=file_id)
        if status.get("fileProcessingStatus") == "COMPLETED":
            break
        sleep(10)  # Wait before checking again

    # Retrieve extracted data
    extracted_data = extraction_agent.extractions.extracted_response(file_id=file_id)
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
- Provides access to `extractions` and `agent_service`.

### `ExtractionManager`
Manage file processing and data extraction.

- **Methods**:
  - `upload_file(file_path: str) -> dict`: Uploads a file and returns its metadata.
  - `start(file_id: str) -> None`: Starts the extraction process for the uploaded file.
  - `processing_status(file_id: str) -> dict`: Retrieves the current status of the processing task.
  - `extracted_response(file_id: str) -> dict`: Fetches the processed data.

### `AgentService`
Manage agents, including creation, updates, retrieval, and deletion.

- **Methods**:
  - `create_agent(agent_payload: CreateAgentInput) -> dict`: Creates a new agent with the specified payload.
    ```python
    from splore_sdk.agents.validations import CreateAgentInput

    agent_payload = CreateAgentInput(agentName="Agent1", description="Sample Agent")
    response = sdk.agent_service.create_agent(agent_payload)
    print(response)
    ```
  - `update_agent(agent_payload: UpdateAgentInput) -> dict`: Updates an existing agent.
    ```python
    from splore_sdk.agents.validations import UpdateAgentInput

    update_payload = UpdateAgentInput(agentId="123", agentName="UpdatedAgent")
    response = sdk.agent_service.update_agent(update_payload)
    print(response)
    ```
  - `get_agents(agentId: Optional[str], agentName: Optional[str]) -> dict`: Retrieves agents based on the provided criteria.
    ```python
    agents = sdk.agent_service.get_agents(agentId="123", agentName=None)
    print(agents)
    ```
  - `delete_agents(agentId: str) -> dict`: Deletes the specified agent.
    ```python
    response = sdk.agent_service.delete_agents(agentId="123")
    print(response)
    ```

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
- Currently, we are supporting PDF files only.

---

## Support

For questions or issues, please open a ticket on [GitHub Issues](https://github.com/splorehq/splore-sdk-py/issues) or email us at support@splore.com.

---

## License

This SDK is licensed under the MIT License. See [LICENSE](LICENSE) for details.