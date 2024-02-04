import requests
from getpass import getpass
from pathlib import Path
import os

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

def main():
    default_repo_url = 'http://default-nexus-repo-url/repository/your-repo-name/'
    repo_url = input(f"Enter Nexus repository URL [{default_repo_url}]: ") or default_repo_url
    username = input("Enter Nexus username: ")
    password = getpass("Enter Nexus password: ")
    auth = (username, password)

    storage_dir = Path('./artifacts-storage/')
    storage_dir.mkdir(parents=True, exist_ok=True)

    artifacts_input = input("Enter artifacts to download (comma-separated, e.g., 'project/binary.version.zip, projectx/binary.version.zip'): ")
    artifacts = parse_artifacts(artifacts_input)

    for artifact in artifacts:
        artifact_url = f"{repo_url}{artifact}"
        local_filename = artifact.split('/')[-1]
        print(f"Downloading {artifact_url} to {storage_dir}...")
        if download_file(artifact_url, local_filename, auth, storage_dir):
            print(f"Successfully downloaded to {storage_dir / local_filename}")
        else:
            print(f"Failed to download {artifact}")

if __name__ == "__main__":
    main()
