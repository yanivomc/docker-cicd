# docker run --add-host eldan-repo.devopshift.com:172.18.0.5 --network docker-cicd_jb -ti  -v "$(pwd)":/resources/ --env FILE_PATH=/resources/entrypoint.sh --env NEXUS_REPO_PROJECT=buildroot --env NEXUS_USER=admin --env NEXUS_PASSWORD=nuva3232 eldan-repo.devopshift.com/binary_manager/binary_manager:1.00.1
import os
import requests
from requests.auth import HTTPBasicAuth

def usage():
    print("---------------------------------------------")
    print(f"The following environment variables must be set: FILE_PATH, NEXUS_REPO_PROJECT, NEXUS_USER, NEXUS_PASSWORD")
    print(f"Optional: NEXUS_BASE_URL (default: https://eldan-repo.devopshift.com/nexus/repository/eldan-raw-repo), BUILD_NUMBER as the suffix for the file name in nexus (default: '')")
    print(f"Example: docker run -ti -v \"$(pwd)\":/resources/ --env FILE_PATH=/resources/entrypoint.sh --env NEXUS_REPO_PROJECT=u-boot  --env NEXUS_USER=admin --env NEXUS_PASSWORD=adminpass eldan-repo.devopshift.com/binary_manager/binary_manager:1.00.1")
    return

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
        # If env BUILD_NUMBER exists, use it as the file name suffix
        if os.getenv('BUILD_NUMBER', '') != '':
            upload_url = f"{nexus_repo_url}/{file_path.split('/')[-1].split('.')[0]}-{os.getenv('BUILD_NUMBER', '')}.{file_path.split('/')[-1].split('.')[1]}"
            upload_url_latest = f"{nexus_repo_url}/{file_path.split('/')[-1].split('.')[0]}-latest.{file_path.split('/')[-1].split('.')[1]}"
        else:
            upload_url = f"{nexus_repo_url}/{file_path.split('/')[-1]}"

        # Make the PUT request to upload the file
        print(f"Uploading {file_path} to {upload_url}...")
        response = requests.put(upload_url, data=file_to_upload, auth=HTTPBasicAuth(nexus_user, nexus_password))
        response_latest = requests.put(upload_url_latest, data=file_to_upload, auth=HTTPBasicAuth(nexus_user, nexus_password))

        # Check if the upload was successful
        if response.status_code == 201:
            print("Upload successful.")
            raise SystemExit(0)
        # Overwrite the file if it already exists
        elif response_latest.status_code == 400:
            print("File already exists. Overwriting...")
            response = requests.put(upload_url_latest, data=file_to_upload, auth=HTTPBasicAuth(nexus_user, nexus_password))
            if response.status_code == 201:
                print("Upload successful.")
                raise SystemExit(0)
            else:
                print(f"Upload failed. Status code: {response.status_code}\n Response: {response.text}")
                raise SystemExit(1)
        if response.status_code == 401:
            print("Auth problem - please check user / pass.")
            raise SystemExit(1)
        else:
            print(f"Upload failed. Status code: {response.status_code}\n Response: {response.text}")
            raise SystemExit(1)

# Grab configuration from os environment variables
file_path = os.getenv('FILE_PATH', '')
# ex: 'http://your-nexus-server/repository/your-repo'
nexus_base_url = os.getenv('NEXUS_BASE_URL', 'https://eldan-repo.devopshift.com/nexus/repository/eldan-raw-repo')
nexus_repo_project = os.getenv('NEXUS_REPO_PROJECT', '')
nexus_repo_url = f"{nexus_base_url}/{nexus_repo_project}"
# DEBUG: 
# print(f"nexus_repo_url: {nexus_repo_url}")
nexus_user = os.getenv('NEXUS_USER', '')
nexus_password = os.getenv('NEXUS_PASSWORD', '')
# Vlidate that all variables are set and not empty strings and let the user know if they are not set correctly
if file_path == '' or nexus_base_url == '' or nexus_repo_project == '' or nexus_user == '' or nexus_password == '':
    print("ERROR: Environment variables are not set or missing.")
    usage()
    raise SystemExit(1)

else:
    upload_to_nexus(file_path, nexus_repo_url, nexus_user, nexus_password)


# TEST:
# upload_to_nexus('/resources/entrypoint.sh', 'https://eldan-repo.devopshift.com/nexus/repository/eldan-raw-repo', 'admin', 'nuva3232')