from splore_sdk.core.exceptions import APIError, ValidationError
from splore_sdk.core.logger import sdk_logger
from splore_sdk.core.validators import FilePathInput
from splore_sdk.extractions.extractions_service import ExtractionService
from splore_sdk.core.api_client import APIClient
import os
import tempfile

class SploreSDK:
    def __init__(self, api_key: str, agent_id:str):
        self.logger = sdk_logger
        if not api_key:
            raise ValueError("API Key is required to initialize SploreSDK.")
        self.agent_id = agent_id
        self.api_key = api_key
        self.logger.info("SploreSDK initialized.")
        self.client = APIClient('https://splore.st', api_key=self.api_key)
        self.extractions = ExtractionService(self.client)

    def upload_file_for_extraction(self, file_path: str, template_id: str):
        """
        Handles file uploads for local files, remote URLs, or AWS S3 paths.
        """
        try:
            payload = FilePathInput(
                file_path=file_path,
                template_id=template_id,
                agent_id=self.agent_id,
            )
            self.logger.info(f"Validated payload: {payload}")
            if os.path.isfile(file_path):
                self.logger.info("Processing local file")
                return self._upload_file(payload.file_path, payload.template_id)
            elif self._is_valid_url(file_path):
                # Remote URL
                self.logger.info("Processing remote URL")
                with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                    self._download_remote_file(file_path, tmp_file.name)
                    return self._upload_file(tmp_file.name, payload.template_id)
            else:
                raise ValidationError("Unsupported file path type")
        except ValidationError as e:
            self.logger.error(f"Validation Error: {e}")
            raise
        except APIError as e:
            self.logger.error(f"API Error: {e}")
            raise

    def _upload_file(self, local_file_path: str, template_id: str):
        """
        Handles the final file upload to the API.
        """
        file_payload = {
            "file_id": self.base_id,
            "agent_id": self.agent_id,
            "template_id": template_id,
        }
        self.logger.info(f"Uploading file: {local_file_path}")
        with open(local_file_path, "rb") as file:
            file_payload["file"] = file
            return self.extractions.upload_file(file_payload)



    

