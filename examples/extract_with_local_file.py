from splore_sdk import SploreSDK

##  example -1 (basic flow to complete extraction local file)
# intialise the sdk with API key and agentId from splore console
sdk = SploreSDK(api_key="", base_id="")
sdk.extract(file_path="/")