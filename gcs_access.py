# One or more routines for accessing Google Cloud Storage
from google.cloud import storage

# Upload files from GCS
def upload_from_GCS(bucket_name, source_blob_name, destination_file_name):
    """Uploads a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)

    blob = bucket.blob(source_blob_name)

    blob.download_to_filename(destination_file_name)

    print('Blob {} uploaded to {}.'.format(
        source_blob_name,
        destination_file_name))
