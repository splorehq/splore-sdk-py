from splore_sdk import SploreSDK

sdk = SploreSDK(api_key="176c6296-6eca-4968-b379-010c1755d791", base_id="STEN2nmgHw3dL5RPlIxJs3zCRuEgslo")
extraction_agent = sdk.init_agent(agent_id="ABSC2nmgKQDsv3EtgxpEEQqb2S9Wajy")
extraction_agent.extract(file_path="/Users/drcom/Downloads/UD0000000030943_XS2800678224_HY_OC_f89c6c9a-325d-4fff-9cb5-04eb65385a2e 1.pdf")
# response = extraction_agent.extractions.all_extracted_response()
# print(response)