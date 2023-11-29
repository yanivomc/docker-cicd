import requests
from getpass import getpass
from pathlib import Path
import os

def download_file(url, local_filename, auth, storage_dir):
    full_path = os.path.join(storage_dir, local_filename)
    with requests.get(url, stream=True, auth=auth) as r:
        r.raise_for_status()
        with open(full_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

def main():
    default_repo_url = 'http://default-nexus-repo-url/repository/your-repo-name/'
    repo_url = input(f"Enter Nexus repository URL [{default_repo_url}]: ") or default_repo_url
    username = input("Enter Nexus username: ")
    password = getpass("Enter Nexus password: ")
    auth = (username, password)

    storage_volume = './artifacts-storage/'
    if not os.path.exists(storage_volume):
        os.makedirs(storage_volume)

    artifacts = input("Enter artifacts to download (comma-separated, e.g., 'project/binary.version.zip, projectx/binary.version.zip'): ")
    if not artifacts:
        if Path('artifacts.list').is_file():
            with open('artifacts.list', 'r') as file:
                artifacts = [line.strip().split('=') for line in file.readlines()]
                artifacts = [f"{proj}/{proj}-{ver}.zip" for proj, ver in artifacts]
        else:
            print("No artifacts specified and 'artifacts.list' file not found.")
            return

    else:
        artifacts = [artifact.strip() for artifact in artifacts.split(',')]

    for artifact in artifacts:
        artifact_url = f"{repo_url}{artifact}"
        local_filename = artifact.split('/')[-1]
        print(f"Downloading {artifact_url} to {storage_volume}...")
        try:
            download_file(artifact_url, local_filename, auth, storage_volume)
            print(f"Downloaded to {storage_volume}{local_filename}")
        except requests.HTTPError as e:
            print(f"Failed to download {artifact}: {e}")

if __name__ == "__main__":
    main()
