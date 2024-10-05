import redis
import hashlib
from datetime import datetime

# Connect to Redis instance
# Ensure Redis is running locally or on the configured server.
r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)


# Function to compute a hash for the given file content
def get_file_hash(file_content: bytes):
    """
    Create a unique hash for the file content.
    This can be used to track duplicates.
    """
    return hashlib.sha256(file_content).hexdigest()


# Function to check if the file is a duplicate
def check_duplicate(file_content: bytes):
    """
    Checks Redis if the file already exists by checking its hash.
    If a duplicate is found, returns the stored metadata.
    """
    file_hash = get_file_hash(file_content)
    if r.exists(file_hash):
        # Retrieve stored metadata if duplicate is found
        file_metadata = r.hgetall(file_hash)
        return {
            "is_duplicate": True,
            "file_metadata": file_metadata
        }
    return {"is_duplicate": False}


# Function to store file metadata in Redis
def store_file_metadata(file_content: bytes, file_path: str, server: str, dataset_name: str):
    """
    Store file hash and metadata in Redis if it's not a duplicate.
    Metadata stored includes the file path, download date, server, and dataset name.
    """
    file_hash = get_file_hash(file_content)
    metadata = {
        "file_path": file_path,
        "download_date": str(datetime.now()),
        "server": server,
        "dataset_name": dataset_name
    }

    # Store the hash and its metadata in Redis
    r.hmset(file_hash, metadata)
    # Optionally, set expiration for the cache (e.g., 1 year)
    r.expire(file_hash, 60 * 60 * 24 * 365)

    return {"status": "file_metadata_stored", "file_hash": file_hash}


# Example usage
if __name__ == "__main__":
    # Example file content - In a real system, this would be the actual file being uploaded/downloaded.
    file_content = b"Example file content"

    # Check if the file is a duplicate
    duplicate_check = check_duplicate(file_content)

    if duplicate_check["is_duplicate"]:
        # If duplicate, alert the user and display stored metadata
        print(f"Duplicate file found! Metadata: {duplicate_check['file_metadata']}")
    else:
        # If not a duplicate, store the file metadata
        stored_metadata = store_file_metadata(
            file_content,
            file_path="/path/to/file",
            server="Server1",
            dataset_name="Dataset_A"
        )
        print("File metadata has been stored:", stored_metadata)
