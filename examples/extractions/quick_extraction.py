from splore_sdk import SploreSDK

# Initialize SDK with API key, base_id from splore console
sdk = SploreSDK(api_key="YOUR_API_KEY", base_id="YOUR_BASE_ID")

# Initialize Agent for extraction
extraction_agent = sdk.init_agent(agent_id="YOUR_AGENT_ID")

# basic extraction flow
extracted_data = extraction_agent.extract(
    file_path="absolute_file_path", max_poll_timeout=600
)
print("Extracted Data:", extracted_data)
