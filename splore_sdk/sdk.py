from time import sleep
from typing import IO, Optional
from splore_sdk.core.logger import sdk_logger
from splore_sdk.extractions.extractions_service import ExtractionService
from splore_sdk.agents.agents_service import AgentService
from splore_sdk.core.api_client import APIClient
from splore_sdk.utils.file_uploader import FileUploader

class SploreSDK:
    def __init__(self, api_key: str, base_id:str, agent_id: Optional[str]):
        self.logger = sdk_logger
        if not api_key:
            raise ValueError("API Key is required to initialize SploreSDK.")
        self.base_id = base_id
        self.api_key = api_key
        self.logger.info("SploreSDK initialized.")
        self.client = APIClient(api_key=self.api_key, base_id=base_id)
        self.extractions = ExtractionService(self.client, agent_id=agent_id)
        self.file_uploader = FileUploader()
        self.agents = AgentService(self.client)
        
    def extract(self, agent_id: str, file_path: Optional[str] = None, file_stream: Optional[IO] = None):
        """run the extraction pipeline by uploading a file.

        Args:
            file_path (Optional[str], optional): provide a local file path if available
            file_stream (Optional[IO], optional): provide a file object/blob if available

        Raises:
            ValueError: One of file_path or file_stream must be provided.

        Returns:
            Dict: extracted response data from the file. 
        """
        if not (file_path or file_stream):
            raise ValueError("One of file_path or file_stream must be provided.")
        if not agent_id:
            raise ValueError("agent_id is required for extraction flow")
        
        self.extractions.set_agent(agent_id=agent_id)
        # upload file using file uploader
        self.logger.info(f"file upload started for file: {file_path}")
        upload_res = self.file_uploader.upload_file(file_path=file_path, file_stream=file_stream)
        self.logger.info(f"file upload completd with file_id: {upload_res}")
        # call start extraction after file upload is completed
        self.extractions.start(file_id=upload_res)
        self.logger.info(f"file extraction started")
        # check status 
        extraction_completed = False
        while(not extraction_completed):
            extraction_resp = self.extractions.processing_status(file_id=upload_res)
            file_processing_status = extraction_resp.get("fileProcessingStatus")
            extraction_completed = (file_processing_status == "COMPLETED")
            self.logger.info(f"file extraction not completed waiting")
            sleep(10)
        
        extracted_resp = self.extractions.extracted_response(file_id=upload_res)
        return extracted_resp


    

