import boto3
from botocore.exceptions import NoCredentialsError

def upload_file_to_s3(file_name, bucket_name, object_name=None):
    """
    Upload a file to an S3 bucket

    Parameters:
        file_name (str): Full local path to the file
        bucket_name (str): Name of the S3 bucket to upload to
        object_name (str): The name the file will have in the S3 bucket. If not specified, file_name is used

    Returns:
        bool: True if file was uploaded, else False
    """
    # Create an S3 client
    s3_client = boto3.client('s3')
    
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    try:
        response = s3_client.upload_file(file_name, bucket_name, object_name)
        print(f"File {file_name} uploaded to {bucket_name}/{object_name}")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False

def get_s3_img_url(bucket_name, object_name):
    """
    Constructs the URL for an image stored in an S3 bucket.

    Parameters:
        bucket_name (str): The name of the S3 bucket
        object_name (str): The name of the object in the bucket

    Returns:
        str: The URL to access the image
    """
    # Assuming the bucket is in the 'us-east-1' region. Change the region if different.
    region_name = 'us-east-1'
    return f"https://{bucket_name}.s3.{region_name}.amazonaws.com/{object_name}"

# Main section to execute the functions
if __name__ == "__main__":
    # Set these values appropriately
    your_bucket_name = 'remote-rehab'
    image_local_path = 'remote-rehab/output/image.jpg'
    image_s3_name = 'your-image-name.jpg'

    # Upload the image to the S3 bucket
    if upload_file_to_s3(image_local_path, your_bucket_name, image_s3_name):
        # If the upload was successful, get the URL of the uploaded image
        url_received = get_s3_img_url(your_bucket_name, image_s3_name)
        print("Uploaded Image URL:", url_received)
