# Import the boto3 library
import boto3
import json
import datetime

# --- Infrastructure Code ---

# Define the AWS region
region_name = 'us-east-1'  # Change this to your desired AWS region

# Create an S3 client
s3_client = boto3.client('s3', region_name=region_name)

# Define the bucket name (make sure it's globally unique)
bucket_name = f'my-jupyter-notebook-bucket-{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}'

try:
    # Create the S3 bucket
    response = s3_client.create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration={'LocationConstraint': region_name}
    )
    print(f"S3 Bucket '{bucket_name}' created successfully!")
    print(json.dumps(response, indent=2))

    # Enable versioning on the bucket
    versioning_response = s3_client.put_bucket_versioning(
        Bucket=bucket_name,
        VersioningConfiguration={'Status': 'Enabled'}
    )
    print(f"Versioning enabled for bucket '{bucket_name}'.")
    print(json.dumps(versioning_response, indent=2))

except Exception as e:
    print(f"Error creating or configuring bucket '{bucket_name}': {e}")

# --- Interactive Exploration and Verification ---

# You can now interact with the created infrastructure using boto3

# List the buckets in your account
print("\n--- Listing S3 Buckets ---")
try:
    list_response = s3_client.list_buckets()
    for bucket in list_response['Buckets']:
        print(f"- {bucket['Name']}")
except Exception as e:
    print(f"Error listing buckets: {e}")

# You can also check the versioning status of the created bucket
print(f"\n--- Checking Versioning Status of '{bucket_name}' ---")
try:
    versioning_status = s3_client.get_bucket_versioning(Bucket=bucket_name)
    print(json.dumps(versioning_status, indent=2))
except Exception as e:
    print(f"Error getting versioning status: {e}")

# --- Optional: Clean up the created resource ---
# Be CAREFUL when running this part, as it will delete the bucket!

# input("\nPress Enter to delete the created bucket...")

# try:
#     # Delete all objects in the bucket (versioned or not)
#     objects = s3_client.list_object_versions(Bucket=bucket_name)
#     if 'Versions' in objects:
#         delete_objects = {'Objects': [{'Key': obj['Key'], 'VersionId': obj['VersionId']} for obj in objects['Versions']]}
#         delete_response = s3_client.delete_objects(Bucket=bucket_name, Delete=delete_objects)
#         print(f"Deleted {len(delete_response.get('Deleted', []))} versions of objects from '{bucket_name}'.")
#     if 'DeleteMarkers' in objects:
#         delete_markers = {'Objects': [{'Key': dm['Key'], 'VersionId': dm['VersionId']} for dm in objects['DeleteMarkers']]}
#         delete_response = s3_client.delete_objects(Bucket=bucket_name, Delete=delete_markers)
#         print(f"Deleted {len(delete_response.get('Deleted', []))} delete markers from '{bucket_name}'.")

#     # Delete the bucket itself
#     delete_bucket_response = s3_client.delete_bucket(Bucket=bucket_name)
#     print(f"S3 Bucket '{bucket_name}' deleted successfully!")
#     print(json.dumps(delete_bucket_response, indent=2))

# except Exception as e:
#     print(f"Error deleting bucket '{bucket_name}': {e}")