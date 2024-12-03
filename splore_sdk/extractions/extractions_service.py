from .validations import StartExtractionInput
from splore_sdk.core.api_client import APIClient

class ExtractionService:
    def __init__(self, api_client: APIClient):
        self.api_client = api_client
    
    def upload_file(self, fileObj):
        return self.api_client.request(method='POST', endpoint='extractions/files', files=fileObj)

    def start(self, file_id: str):
        payload = StartExtractionInput(
            agent_id=self.api_client.agent_id,
            file_id=file_id,
        )
        return self.api_client.request(method='POST', endpoint='extractions/start', json=payload.model_dump())
    
    def processing_status(self, file_id: str):
       params = {
            'agentId': self.api_client.agent_id,
            'fileId': file_id
        }
       return self.api_client.request(method='GET', endpoint='extractions/status', params=params)
    def extracted_response(self, file_id:str):
        params = {
            'agentId': self.api_client.agent_id,
            'fileId': file_id
        }
        return self.api_client.request(method='GET', endpoint='extractions', params=params)
    def all_extracted_response(self):
        return self.api_client.request(method='GET', endpoint='extractions')
    
    
