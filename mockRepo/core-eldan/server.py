import os
import shutil
import subprocess
from pathlib import Path
import gspread
from xml.etree import ElementTree as ET

# Set Environment Variables
NEXUS_API_KEY = os.environ.get('NEXUS_API_KEY', '20a4b826-31aa-3ab7-a0b1-cb3fd9fbfa7e')
BUILD_NUMBER = os.environ.get('BUILD_NUMBER' , '1.00.1')
# Function to process a job
def process_job(job_id, jobs_list, processed_jobs):
    # Attempt to find the job by ID
    job = next((item for item in jobs_list if item["JobID"] == job_id), None)

    if job['Depends'] == "NONE":
        print(f"JobID: {job_id} ('{job['Name']}') has no dependencies and is part of docker bake process. skipping...")
        processed_jobs.add(job_id)
        return

    # If job has already been processed or doesn't exist, return early
    if job_id in processed_jobs:
        print(f"JobID: {job_id} already processed. Skipping...")
        return
    if not job:
        print(f"JobID: {job_id} not found. Skipping...")
        return

    if job["Name"] not in os.listdir('./mockRepo/core-eldan/src/'):
        os.mkdir(f'./mockRepo/core-eldan/src/{job["Name"]}')
        copy_files(job_id, job["Name"])
    else:
        copy_files(job_id, job["Name"])
    # Log if job has dependencies
    if job["Depends"] != "NONE":
        print(f"JobID: {job_id} ('{job['Name']}') has dependencies: {job['Depends']}. Processing dependencies first...")
        dependencies = [int(dep) for dep in job["Depends"].split(", ")]
        # Call add dependency function to add the dependency to the Core.{job[Name]}.csproj file base on the job_name
        print(f"Adding dependency for JobID: {job_id} ('{job['Name']}') to Core.{job['Name']}.csproj file...")
        add_dependency_to_csproj(job_id, job["Name"], dependencies, jobs_list)
        for dep in dependencies:
            # Run the process_job function for the dependency
            process_job(dep, jobs_list, processed_jobs)


    else:
        print(f"JobID: {job_id} ('{job['Name']}') has no dependencies and is part of docker bake process. skipping...")
        processed_jobs.add(job_id)
        return

    # Now process the current job
    print(f"Processing JobID: {job_id} ('{job['Name']}').")
    # Run the docker build command and log the output to the console as json format.
    # Catch docker build errors and log them to the console in json and continue processing the next job.
    # Json structure should be { "JobID": 1, "Name": "DataAccess", "Status": "Success" , "Error": "" , timeofexecution: ""2021-09-01T12:00:00Z"" }
    # Docker command: docker build  --build-arg NEXUS_API_KEY=20a4b826-31aa-3ab7-a0b1-cb3fd9fbfa7e --build-arg BUILD_NUMBER=1.00.1 -t {jobname} -f dockerfile .
    job_name = job["Name"].lower()
    docker_build_command = f"cd ./mockRepo/core-eldan/src/{job_name}/ && docker build --build-arg NEXUS_API_KEY=20a4b826-31aa-3ab7-a0b1-cb3fd9fbfa7e --build-arg BUILD_NUMBER=1.00.1 -t {job_name} -f dockerfile ."
    try:
        print(f"Running docker build command for JobID: {job_id} ('{job['Name']}')...")
        output = subprocess.check_output(docker_build_command, shell=True, text=True)
        print(f"JobID: {job_id} ('{job['Name']}') build successful.")
    except subprocess.CalledProcessError as e:
        output = (f"JobID: {job_id} ('{job['Name']}') build failed. Error: {e.output}")
        print (output)
        # Write the error to a file jobfailure_date_time.txt
        with open(f'jobfailure_{job_id}.txt', 'w') as f:
            f.write(output)

        

    # Mark current job as processed
    processed_jobs.add(job_id)

def add_dependency_to_csproj(job_id, job_name, dependencies, jobs_list):
    csproj_path = f'./mockRepo/core-eldan/src/{job_name}/Core.{job_name}.csproj'
    ET.register_namespace('', 'http://schemas.microsoft.com/developer/msbuild/2003')
    
    tree = ET.parse(csproj_path)
    root = tree.getroot()
    
    # Find the last ItemGroup that contains PackageReference
    package_item_groups = [ig for ig in root.findall('{http://schemas.microsoft.com/developer/msbuild/2003}ItemGroup') if ig.find('{http://schemas.microsoft.com/developer/msbuild/2003}PackageReference') is not None]
    
    if not package_item_groups:
        # If no ItemGroup with PackageReference exists, create a new one
        item_group = ET.SubElement(root, 'ItemGroup')
    else:
        # Otherwise, use the last one found
        item_group = package_item_groups[-1]
    
    existing_packages = {pkg.get('Include'): pkg for pkg in item_group.findall('{http://schemas.microsoft.com/developer/msbuild/2003}PackageReference')}
    
    for dep in dependencies:
        # Lookup job name using job_id from jobs_list
        job_info = next((item for item in jobs_list if item["JobID"] == dep), None)
        if job_info:
            dep_name = f"Core.{job_info['Name']}"
            if dep_name not in existing_packages:
                ET.SubElement(item_group, '{http://schemas.microsoft.com/developer/msbuild/2003}PackageReference', attrib={'Include': dep_name, 'Version': '*'})
                print(f"Added {dep_name} to {csproj_path}.")
            else:
                print(f"{dep_name} already exists in {csproj_path}.")
    
    # Write changes back to the .csproj file
    tree.write(csproj_path, encoding='utf-8', xml_declaration=True)


def copy_files(job_id, job_name):
    if job_name == "DataAccess":
        print(f"JobID: {job_id} ('{job_name}') is DataAccess. Skipping copying files...")
        return
    source_dir = Path('./mockRepo/core-eldan/src/DataAccess')
    destination_dir = Path(f'./mockRepo/core-eldan/src/{job_name}')

    print(f"Copying files for JobID: {job_id} ('{job_name}') from {source_dir} to {destination_dir}...")

    if destination_dir.exists():
        shutil.rmtree(destination_dir)
    shutil.copytree(source_dir, destination_dir)

    # Replace DataAccess with job_name in the copied files
    files = list(destination_dir.rglob('*.*'))  # Assuming you want to replace in all files, adjust the pattern as needed

    for file in files:
        with open(file, 'r') as f:
            filedata = f.read()

        filedata = filedata.replace('DataAccess', job_name)

        with open(file, 'w') as f:
            if file.name == "Core.DataAccess.csproj":
                # change the file name to match the job name
                f.write(filedata.replace('DataAccess', job_name))
                os.rename(file, file.parent / f"Core.{job_name}.csproj")
            else:
             f.write(filedata)

    print(f"Files copied and replacements made for JobID: {job_id} ('{job_name}').")
    


# Main logic
def main():
    # Initialize gspread client and open spreadsheet
    service_account_file_paths = ['./mockRepo/core-eldan/service-account.json', '/app/service-account.json', './service-account.json']
    for path in service_account_file_paths:
        if os.path.exists(path):
            gc = gspread.service_account(filename=path)
            break
    else:
        print("Service account file not found.")
        exit(1)
    
    # gc = gspread.service_account(filename='./mockRepo/core-eldan/service-account.json')
    spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1qkWADi9XRcHSu3RcpvYGwJ2Jr6UCKi-Xt6KeevvItWY/edit?usp=sharing'
    sh = gc.open_by_url(spreadsheet_url)
    worksheet = sh.sheet1
    values = worksheet.get_all_values()
    
    # Create a list of job dictionaries
    jobs_list = [{"JobID": i+1, "Name": row[0], "order": row[1], "Depends": row[2]} for i, row in enumerate(values[1:])]
    
    # Set to track processed jobs
    processed_jobs = set()
    
    print("Starting job processing...")
    # Process each job, respecting dependencies
    for job in jobs_list:
        process_job(job["JobID"], jobs_list, processed_jobs)
    print("All jobs processed.")

if __name__ == "__main__":
    main()
