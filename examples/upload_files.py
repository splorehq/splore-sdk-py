from splore_sdk import SploreSDK

# Initialize SDK
sdk = SploreSDK(api_key="d941e8a9-6109-4724-a416-bf303610cacc", base_id="STEN2sZRhaR7x65dNdAE8YrDRZC3DkW")


# Open and upload file
with open("/Users/drcom/codes/splore/splore-sdk-py/UD0000000035067_OC.pdf", "rb") as file:
    response = sdk.file_uploader.upload_file(file_stream=file)
    print("Upload Response:", response)