from splore_sdk import SploreSDK

sdk = SploreSDK(api_key="176c6296-6eca-4968-b379-010c1755d791", base_id="STEN2nmgHw3dL5RPlIxJs3zCRuEgslo")
response = sdk.get_agents(agentId="ABSC2pO7PXHeknC91c19HKVzY8rIPbf")
print(response)