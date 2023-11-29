import os
import requests
from requests.auth import HTTPBasicAuth

def upload_to_nexus(file_path, nexus_repo_url, nexus_user, nexus_password):
    """
    Uploads a file to a Nexus repository.

    Args:
    file_path (str): The path to the file to upload.
    nexus_repo_url (str): The URL of the Nexus repository.
    nexus_user (str): Nexus username.
    nexus_password (str): Nexus password.
    """

    # Open the file in binary mode
    with open(file_path, 'rb') as file_to_upload:
        # Define the URL for the upload
        upload_url = f"{nexus_repo_url}/{file_path.split('/')[-1]}"

        # Make the PUT request to upload the file
        response = requests.put(upload_url, data=file_to_upload, auth=HTTPBasicAuth(nexus_user, nexus_password))

        # Check if the upload was successful
        if response.status_code == 201:
            print("Upload successful.")
        else:
            print(f"Upload failed. Status code: {response.status_code}\nResponse: {response.text}")

# Grab configuration from os environment variables
file_path = os.environ['FILE_PATH']
# ex: 'http://your-nexus-server/repository/your-repo'
nexus_repo_url = os.environ['NEXUS_REPO_URL']
nexus_user = os.environ['NEXUS_USER']
nexus_password = os.environ['NEXUS_PASSWORD']
# Vlidate that all variables are set and not empty strings and let the user know if they are not set correctly
if not file_path:
    print("FILE_PATH environment variable not set.")
    raise SystemExit(1)
elif not nexus_repo_url:
    print("NEXUS_REPO_URL environment variable not set.")
    raise SystemExit(1)
elif not nexus_user:
    print("NEXUS_USER environment variable not set.")
    raise SystemExit(1)
elif not nexus_password:
    print("NEXUS_PASSWORD environment variable not set.")
    raise SystemExit(1)
else:
    upload_to_nexus(file_path, nexus_repo_url, nexus_user, nexus_password)
