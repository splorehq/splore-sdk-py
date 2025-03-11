from splore_sdk import __version__
print("Splore SDK Version:", __version__)
# Importing the SploreSDK class from the splore_sdk module
print()
sdk = SploreSDK(api_key = "19c74cec-c7d0-46be-9e13-8d6c90c84f2a",base_id = "STEN2e2WJpBB9B2Xa9fb9GSpHNXuRqU")
agents = sdk.agents.get_agents(agentId="ABSC2s3iTPIe41JFnluTC9WeceSIFEj")
print(agents)