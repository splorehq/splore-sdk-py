# Splore Python SDK  

The Splore Python SDK simplifies the process of interacting with the Splore document processing platform. Use it to upload files, process documents, and retrieve extracted data with minimal setup.

---

## 📌 Table of Contents  

- [Features](#features)  
- [Installation](#installation)  
- [Getting Started](#getting-started)  
- [Modules Overview](#modules-overview)  
  - [Agent Management](#agent-management)  
  - [Extractions](#extractions)  
  - [File Upload](#file-upload)  
  - [Search](#search)  
- [Advanced Usage](#advanced-usage)  
- [FAQ](#faq)  
- [Support](#support)  
- [License](#license)  

---

## 🚀 Features  

- **Agent Management**: Create, update, retrieve, and delete agents.  
- **File Upload**: Upload documents for processing.  
- **Extractions**: Extract structured data from documents.  
- **Search**: Perform web searches and retrieve search history.  
- **AWS S3 Integration**: Process files directly from S3.  
- **Task Monitoring**: Track the progress of extraction jobs.  
- **Error Handling**: Provides meaningful errors and retry mechanisms.  
- **Python 3.7+ Compatibility**: tested supported version after 3.7.17 can be used for python 3.7 and above.

---

## 📥 Installation  

Install the SDK via pip:  

```bash
pip install splore-sdk
```

For optional example dependencies:  

```bash
pip install splore-sdk[examples]
```

---

## 🏁 Getting Started  

### Prerequisites  

1. **API Key and Base ID**: Obtain these from the Splore console.  
2. **Python 3.7+**: Ensure Python is installed.  

### Quick Start Example

```python
from splore_sdk import SploreSDK

# Initialize SDK
sdk = SploreSDK(api_key="YOUR_API_KEY", base_id="YOUR_BASE_ID")

# Initialize Agent for extraction
extraction_agent = sdk.init_agent(agent_id="YOUR_AGENT_ID")

# Basic extraction flow
extracted_response = extraction_agent.extract(file_path="absolute_file_path")
print(extracted_response)
```

---

## 📦 Modules Overview  

### 🔹 [Agent Management](#agent-management)  

Manage agents for document processing.  

#### Example Usage  

```python
from splore_sdk import SploreSDK

# Initialize SDK
sdk = SploreSDK(api_key="YOUR_API_KEY", base_id="YOUR_BASE_ID")

# Create an agent
agent_payload = {"name": "Test Agent", "config": {"key": "value"}}
create_response = sdk.create_agent(agent_payload)
print("Create Agent Response:", create_response)

# Get agent details
agent_id = create_response.get("id")
get_response = sdk.agents.get_agents(agentId=agent_id)
print("Get Agent Response:", get_response)

# Get all agents
all_agents = sdk.agents.get_agents()
print("All Agents:", all_agents)

# Update the agent
update_payload = {"name": "Updated Agent Name"}
update_response = sdk.agents.update_agent(agent_payload=update_payload)
print("Update Agent Response:", update_response)

# Delete the agent
delete_response = sdk.agents.delete_agents(agentId=agent_id)
print("Delete Agent Response:", delete_response)
```

### 🔹 [Extractions](#extractions)  

Handle document processing and extraction.  

#### Example Usage

```python
from splore_sdk import SploreSDK
from time import sleep

# Initialize SDK
sdk = SploreSDK(api_key="YOUR_API_KEY", base_id="YOUR_BASE_ID")

# Get all agents
agents = sdk.agents.get_agents()
agent_id = agents[0]["id"]  # Adjust as needed

# Initialize agent
extraction_agent = sdk.init_agent(agent_id=agent_id)

# Upload file
upload_response = extraction_agent.file_uploader.upload_file(file_path="path/to/file.pdf")
file_id = upload_response
print("File uploaded with ID:", file_id)

# Start extraction
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

### 🔹 [Search](#search)  

Perform web searches and manage search history.  

#### Example Usage

```python
from splore_sdk import SploreSDK

# Initialize SDK
sdk = SploreSDK(api_key="YOUR_API_KEY", base_id="YOUR_BASE_ID")

# Initialize agent
agent_id = "YOUR_AGENT_ID"
search_agent = sdk.init_agent(agent_id=agent_id)

# Perform a search
search_results = search_agent.search.search(query="artificial intelligence", count=5, engine="google")
print("Search Results:", search_results)

# Get search history
history = search_agent.search.get_history(page=0, size=10)
print("Search History:", history)
```

### 🔹 [File Upload](#file-upload)  

Upload files to Splore for processing.  

#### Example Usage

```python
from splore_sdk import SploreSDK

# Initialize SDK
sdk = SploreSDK(api_key="YOUR_API_KEY", base_id="YOUR_BASE_ID")

# Upload file with metadata
metadata = {
    "file_name": "document.pdf",
    "custom_extraction": "false",
    "is_data_file": "true"
}

with open("path/to/file.pdf", "rb") as file:
    response = sdk.file_uploader.upload_file(file_stream=file, metadata=metadata)
    print("Upload Response:", response)
```

### 🔹 [AWS Integration](#aws-integration)  

Download files from AWS S3 for extraction.  

#### Example Usage

```python
from splore_sdk import SploreSDK
from examples.aws import download_from_s3

# Initialize SDK
sdk = SploreSDK(api_key="YOUR_API_KEY", base_id="YOUR_BASE_ID")

# Initialize extraction agent
extraction_agent = sdk.init_agent(agent_id="YOUR_AGENT_ID")

# Create a temporary file destination
file_ref = sdk.file_uploader.create_temp_file_destination(file_extension=".pdf")
s3_uri = "s3://abc/def/abc.pdf"

# Download file from S3
download_from_s3(s3_uri, file_ref)

# Start extraction
response = extraction_agent.extract(file_path=file_ref)
print("Extraction Response:", response)
```

---

## ⚙️ Advanced Usage  

### 🔸 Polling Interval Configuration  

Customize the polling interval for extraction status checks.  

```python
while True:
    status = sdk.extractions.processing_status(file_id=file_id)
    if status.get("fileProcessingStatus") == "COMPLETED":
        break
    sleep(5)  # Set custom polling interval
```

### 🔸 Error Handling  

Handle errors gracefully for better debugging.  

```python
try:
    sdk.extractions.upload_file("path/to/file.pdf")
except Exception as e:
    print("Error uploading file:", str(e))
```

### 🔸 Python 3.7 Compatibility  

The SDK now supports Python 3.7 and above.

---

## ❓ FAQ  

### 1️⃣ How do I get an API Key?  
Sign up on the Splore console and navigate to the API section to generate a key.  

### 2️⃣ Can I use this SDK asynchronously?  
Asynchronous support will be added in a future release.  

### 3️⃣ Which file formats are supported?  
Currently, only **PDF files** are supported.  

### 4️⃣ How do I handle search functionality?  
The SDK provides a dedicated `search` capability that allows you to perform web searches and manage search history. Use the `search.search()` method to perform searches and `search.get_history()` to retrieve search history.  

### 5️⃣ How do I check the SDK version?  
```python
from splore_sdk import __version__
print("Splore SDK Version:", __version__)
```

---

## 🔗 Support  

For any questions or issues, please:  

- Open a ticket on [GitHub Issues](https://github.com/splorehq/splore-sdk-py/issues)  
- Email us at **support@splore.com**  

---

## 📜 License  

This SDK is licensed under the MIT License. See [LICENSE](LICENSE) for details.
