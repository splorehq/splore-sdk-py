import os
import tempfile
from typing import Optional, IO, Dict
from splore_sdk.core.constants import FILE_UPLOAD_URL
from tusclient import client
import mimetypes


class FileUploader:
    def __init__(self, auto_cleanup: bool = True):
        """
        Initializes the FileUploader instance.

        Args:
            auto_cleanup (bool): Whether to automatically clean up temporary files.
        """
        self.tus_client = client.TusClient(FILE_UPLOAD_URL)
        self.temp_files = []
        self.auto_cleanup = auto_cleanup

    def create_temp_file_destination(self) -> str:
        """
        Creates a temporary file destination path to be used for downloads.

        Returns:
            str: Path to the temporary file.
        """
        tmp_file = tempfile.NamedTemporaryFile(delete=False)
        tmp_file.close()
        self.temp_files.append(tmp_file.name)
        return tmp_file.name

    def generate_default_metadata(self, file_path: str) -> Dict[str, str]:
        """
        Generates default metadata for the uploaded file.

        Args:
            file_path (str): The path of the file to upload.

        Returns:
            Dict[str, str]: Default metadata including filename, filetype, and customExtractionEnabled.
        """
        filename = os.path.basename(file_path)
        filetype = os.path.splitext(filename)[1][1:]
        mime_type, _ = mimetypes.guess_file_type(file_path)
        filetype = mime_type if mime_type else filetype

        return {
            "filename": filename,
            "filetype": filetype,
            "customExtractionEnabled": "true",
            "isDataFile": "true"
        }

    def encode_metadata(self, metadata: Dict[str, any]) -> Dict[str, str]:
        """
        Ensures metadata is in a string-encoded format suitable for upload.

        Args:
            metadata (Dict[str, any]): Metadata dictionary.

        Returns:
            Dict[str, str]: String-encoded metadata dictionary.
        """
        return {key: str(value) for key, value in metadata.items()}

    def upload_file(self, file_path: Optional[str] = None, file_stream: Optional[IO] = None, metadata: Optional[dict] = None) -> str:
        """
        Uploads a file to the TUS server using various input options.

        Args:
            file_path (Optional[str]): Local file path to upload.
            file_stream (Optional[IO]): File stream (e.g., from blob storage).
            metadata (Optional[dict]): Metadata to include with the upload.

        Returns:
            str: return file_id.

        Raises:
            ValueError: If neither file_path nor file_stream is provided.
        """
        if not (file_path or file_stream):
            raise ValueError("One of file_path or file_stream must be provided.")

        temp_file_path = None

        try:
            # Determine the file path
            if file_path:
                temp_file_path = os.path.normpath(os.path.abspath(file_path))
            elif file_stream:
                temp_file_path = self.create_temp_file_destination()
                self._write_stream_to_tmp(file_stream, temp_file_path)

            # Generate default metadata and merge with user-provided metadata
            default_metadata = self.generate_default_metadata(temp_file_path)
            final_metadata = {**default_metadata, **(metadata or {})}
            encoded_metadata = self.encode_metadata(final_metadata)

            # Upload to TUS server
            chunk_size = 5 * 1024 * 1024 # 5MB chunk size
            uploader = self.tus_client.uploader(file_path=temp_file_path, metadata=encoded_metadata, chunk_size=chunk_size)
            uploader.upload()

            # Return the file id
            url_with_file_id = uploader.url.split("+")[0]
            return url_with_file_id.split("/")[-1] 

        finally:
            if self.auto_cleanup and temp_file_path and temp_file_path in self.temp_files:
                self.cleanup_temp_files()

    def _write_stream_to_tmp(self, file_stream: IO, tmp_path: str):
        """
        Writes a file stream to a temporary file.

        Args:
            file_stream (IO): The input file stream.
            tmp_path (str): Path to the temporary file.
        """
        with open(tmp_path, 'wb') as tmp_file:
            tmp_file.write(file_stream.read())

    def cleanup_temp_files(self):
        """
        Deletes all temporary files tracked by the uploader.
        """
        for file_path in self.temp_files:
            try:
                os.remove(file_path)
            except OSError:
                pass
        self.temp_files.clear()

