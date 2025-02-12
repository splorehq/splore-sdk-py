from splore_sdk import SploreSDK

# Initialize SDK
sdk = SploreSDK(api_key="YOUR_API_KEY", base_id="YOUR_BASE_ID")


# Open and upload file
with open("path/to/your/file.pdf", "rb") as file:
    response = sdk.file_uploader.upload_file(file_stream=file)
    print("Upload Response:", response)