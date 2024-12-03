from time import sleep
from splore_sdk import SploreSDK
import tempfile

from examples.aws import download_from_s3


# intialise the sdk with API key and agentId from splore console
sdk = SploreSDK(api_key="", agent_id="")
 
# download the file from aws s3.
with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
    s3_uri = "s3://abc/def/abc.pdf"
    download_from_s3(s3_uri, tmp_file.name)
    file_upload_response = sdk.extractions.upload_file(tmp_file.file)
    file_id = file_upload_response.get('file_id')
    if file_id is None:
        raise RuntimeError("upload failed")
    
    # start extractions
    sdk.extractions.start(file_id=file_id)
    
    # check status 
    extraction_completed = False
    while(not extraction_completed):
        extraction_resp = sdk.extractions.processing_status(file_id=file_id)
        file_processing_status = extraction_resp.get("fileProcessingStatus")
        extraction_completed = (file_processing_status == "COMPLETED")
        sleep(10)
        
    extracted_resp = sdk.extractions.extracted_response(file_id=file_id)
    print(extraction_resp)
        
    
    
