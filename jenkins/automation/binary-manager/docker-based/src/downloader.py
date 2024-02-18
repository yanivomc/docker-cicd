from requests.auth import HTTPBasicAuth
import requests
from getpass import getpass
from pathlib import Path
import os
# Get environment variables from .env file
from dotenv import load_dotenv
load_dotenv()
# Print all environment variables from .env file
# print(os.environ)
# set SWNEXUSFOLDER to the evnironment variable SWNEXUSFOLDER or default to none
SWNEXUSFOLDER = os.getenv('SWNEXUSFOLDER', None)
KERNELNEXUSFOLDER= os.getenv('KERNELNEXUSFOLDER', None)
UBOOTNEXUSFOLDER= os.getenv('UBOOTNEXUSFOLDER', None)
DEFAULTNEXUSURI= os.getenv('DEFAULTNEXUSURI', None)
BUILDEROOTNEXUSFOLDER= os.getenv('BUILDEROOTNEXUSFOLDER', None)




def download_file(url, local_filename, auth, storage_dir):
    storage_path = storage_dir / local_filename
    try:
        with requests.get(url, stream=True, auth=auth) as r:
            r.raise_for_status()
            with open(storage_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
    except (requests.ConnectionError, requests.Timeout, requests.HTTPError) as e:
        print(f"Error downloading file {local_filename}: {e}")
        return False
    return True

def parse_artifacts(input_artifacts):
    if input_artifacts:
        return [artifact.strip() for artifact in input_artifacts.split(',')]
    elif Path('artifacts.list').is_file():
        with open('artifacts.list', 'r') as file:
            return [f"{proj.strip()}/{ver.strip()}.zip" for proj, ver in (line.split('=') for line in file)]
    else:
        print("No artifacts specified and 'artifacts.list' file not found.")
        return []

# Function to validate login credentials
def validate_login(auth,repo_url=DEFAULTNEXUSURI):
    # cut repo_url to base url
    repo_url = repo_url.split('/repository')[0]
    try:
        response = requests.get(repo_url, auth=auth)
        response.raise_for_status()
        return True
    except requests.HTTPError as e:
        print(f"Error: {e}")
        return False
# Validate login credentials
   

# Function to get latest added artifact from nexus repository
def get_latest_artifact(username,password,repo_url):
    project_names= [SWNEXUSFOLDER,KERNELNEXUSFOLDER,UBOOTNEXUSFOLDER,BUILDEROOTNEXUSFOLDER]
    fileList= []
    # Authentication for Nexus Repository
    auth = HTTPBasicAuth(username, password)
    # exract the folder name from the repo_url (http://localhost:8081/nexus/repository/[FOLDERNAME/)
    print(f"Repo URL: {repo_url}")
    repo_name = repo_url.split('/')[-3]
    print(f"Repo name: {repo_name}")
    repo_url = repo_url.split('/repository')[0]
    print(f"Repo name: {repo_url}")
    


    # Adjust this URL to search within a specific repository
    search_url = f"{repo_url}/service/rest/v1/search/assets"
    
    try:
        for files in project_names:
        # Adjust parameters as needed, for example, to filter by format or name
            print(f"Searching for latest assets in the repository {files}...")
            params = {
                'repository': repo_name,
                'name': '*latest*',  # Filter by files ending with .latest
                'group': files,  # Assuming you want to filter by group. Adjust as necessary.
            }
            print(f"Params: {params}")
            response = requests.get(search_url, auth=auth, params=params)
            response.raise_for_status()
            
            # Assuming the response is JSON and contains a list of assets
            assets = response.json().get('items', [])
            
            if not assets:
                print(f"No assets found in the repository {files} - skipping.")
                continue
            

            
            # Assuming the assets are returned in the desired order, get the first one
            latest_asset = assets[0]  # Adjust based on how the sorting is actually applied
            # add the latest asset to the files list
            fileList.append(latest_asset['path'])
            print("**************************************************")
            print(f"\nLatest assets found:\n {latest_asset['path']}\n")
            print(f"--------------------------------------------------\n")
        # Return the name (path) of the latest asset
        return fileList
    except requests.HTTPError as e:
        print(f"Failed to fetch assets: {e}")
        return None
  

def main():
    default_repo_url = DEFAULTNEXUSURI
    repo_url = input(f"Enter Nexus repository URL [{default_repo_url}]: ") or default_repo_url
    username = input("Enter Nexus username: ")
    password = getpass("Enter Nexus password: ")
    auth = (username, password)
    if not validate_login(auth,repo_url):
        print("Invalid login credentials. Please retry...")
        main()
    

    storage_dir = Path('./artifacts-storage/')
    storage_dir.mkdir(parents=True, exist_ok=True)

    artifacts_input = input("Enter artifacts to download ('latest' for all latest artifacts , comma-separated, e.g., 'project/binary.version.zip, projectx/binary.version.zip'): ")
    artifacts = parse_artifacts(artifacts_input)
    if 'latest' in artifacts:
        latest_artifact = get_latest_artifact(username,password,repo_url)
        if latest_artifact:
            artifacts = latest_artifact
        else:
            print("Failed to fetch latest artifact. Exiting...")
            return
    for artifact in artifacts:
        artifact_url = f"{repo_url}{artifact}"
        local_filename = artifact.split('/')[-1]
        print(f"Downloading {artifact_url} to {storage_dir}...")
        if download_file(artifact_url, local_filename, auth, storage_dir):
            print(f"Successfully downloaded to {storage_dir / local_filename}")
        else:
            print(f"Failed to download {artifact}")

if __name__ == "__main__":
    # main()
    # catch ctrl+c to prevent the program from exiting with an error
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\nExiting...")
        exit(0)
    except Exception as e:
        # print new line

        print(f"\n\nAn error occurred: {e}")
        exit(1)
