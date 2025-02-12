import pytest
from unittest.mock import MagicMock, patch
from splore_sdk.core.api_client import APIClient
from splore_sdk.utils.file_uploader import FileUploader
from splore_sdk.extractions.extractions_service import ExtractionService
from splore_sdk.agents.agents_service import AgentService
from splore_sdk import SploreSDK, AgentSDK

@pytest.fixture
def splore_sdk():
    with patch("splore_sdk.core.api_client.APIClient") as MockAPIClient, \
         patch("splore_sdk.utils.file_uploader.FileUploader") as MockFileUploader, \
         patch("splore_sdk.agents.agents_service.AgentService") as MockAgentService:
        
        mock_client = MockAPIClient.return_value
        mock_file_uploader = MockFileUploader.return_value
        mock_agent_service = MockAgentService.return_value
        
        return SploreSDK("test_api_key", "test_base_id")

def test_init_without_api_key():
    with pytest.raises(ValueError):
        SploreSDK("", "test_base_id")

def test_get_agents(splore_sdk):
    splore_sdk.agents.get_agents = MagicMock(return_value=[{"id": "agent_1", "name": "Test Agent"}])
    agents = splore_sdk.get_agents()
    assert len(agents) == 1
    assert agents[0]["id"] == "agent_1"

def test_init_agent(splore_sdk):
    agent_sdk = splore_sdk.init_agent("test_agent_id")
    assert isinstance(agent_sdk, AgentSDK)
    assert agent_sdk.agent_id == "test_agent_id"

def test_init_agent_without_id(splore_sdk):
    with pytest.raises(ValueError):
        splore_sdk.init_agent("")

@pytest.fixture
def agent_sdk():
    with patch("splore_sdk.extractions.extractions_service.ExtractionService") as MockExtractionService, \
         patch("splore_sdk.core.api_client.APIClient") as MockAPIClient, \
         patch("splore_sdk.utils.file_uploader.FileUploader") as MockFileUploader:
        
        mock_client = MockAPIClient.return_value
        mock_file_uploader = MockFileUploader.return_value
        mock_extraction_service = MockExtractionService.return_value
        
        return AgentSDK("test_api_key", "test_base_id", "test_agent_id")

def test_extract_without_file(agent_sdk):
    with pytest.raises(ValueError):
        agent_sdk.extract()

def test_extract(agent_sdk):
    agent_sdk.extractions.set_agent = MagicMock()
    agent_sdk.file_uploader.upload_file = MagicMock(return_value="file_123")
    agent_sdk.extractions.start = MagicMock()
    agent_sdk.extractions.processing_status = MagicMock(return_value={"fileProcessingStatus": "COMPLETED"})
    agent_sdk.extractions.extracted_response = MagicMock(return_value={"data": "extracted"})
    
    result = agent_sdk.extract(file_path="test.pdf")
    assert result == {"data": "extracted"}
