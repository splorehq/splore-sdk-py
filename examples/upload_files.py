from splore_sdk import SploreSDK

# Initialize SDK
sdk = SploreSDK(api_key="c9a50980-08b1-4a5a-b4ef-60220abb94d4", base_id="STEN2qemZ3IizHabc9rcpa5VtNNk7Nu")


# Open and upload file
# use unix based file path.
with open("/Users/drcom/codes/splore/splore-sdk-py/examples/UD0000000035067_OC.pdf", "rb") as file:
    response = sdk.file_uploader.upload_file(file_stream=file)
    print("Upload Response:", response)