from typing import Optional
import requests
from .exceptions import APIError
from .logger import sdk_logger
from .constants import BASE_URL

class APIClient:
    def __init__(self, api_key: str, base_id: str, agent_id: Optional[str], base_url: Optional[str]):
        self.api_key = api_key
        self.agent_id = agent_id
        self.base_id = base_id
        self.base_url = base_url if base_url else BASE_URL
        self.logger = sdk_logger
        self.logger.debug(f"api client initialised with api_key:${self.api_key}, base_url: ${base_url}")
        
        
    def request(self, method: str, endpoint: str, **kwargs):
        headers = kwargs.pop("headers", {})
        headers["X-API-KEY"] = self.api_key
        url = f"{self.base_url}/{endpoint}"
        try:
            self.logger.debug(f"api with url: {url}, method: {method} \n headers: {headers} \n started")
            response = requests.request(method, url, headers=headers, **kwargs)
            response.raise_for_status()
            self.logger.info(f"api with endpoint: {endpoint}, {method.upper()} succeeded")
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error()
            raise APIError(f"API Request {url}, method: {method} failed: {e}")