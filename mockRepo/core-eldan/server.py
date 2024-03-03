import os
import gspread

# Function to process a job
def process_job(job_id, jobs_list, processed_jobs):
    # Attempt to find the job by ID
    job = next((item for item in jobs_list if item["JobID"] == job_id), None)

    # If job has already been processed or doesn't exist, return early
    if job_id in processed_jobs:
        print(f"JobID: {job_id} already processed. Skipping...")
        return
    if not job:
        print(f"JobID: {job_id} not found. Skipping...")
        return

    # Log if job has dependencies
    if job["Depends"] != "NONE":
        print(f"JobID: {job_id} ('{job['Name']}') has dependencies: {job['Depends']}. Processing dependencies first...")
        dependencies = [int(dep) for dep in job["Depends"].split(", ")]
        for dep in dependencies:
            process_job(dep, jobs_list, processed_jobs)
    else:
        print(f"JobID: {job_id} ('{job['Name']}') has no dependencies and is part of docker bake process. skipping...")
        processed_jobs.add(job_id)
        return

    # Now process the current job
    print(f"Processing JobID: {job_id} ('{job['Name']}').")
    # Create job name folder in the mockRepo/core-eldan folder if it doesn't exist
    print(f"Creating folder for JobID: {job_id} ('{job['Name']}') in mockRepo/core-eldan folder...")
    if job["Name"] not in os.listdir('./mockRepo/core-eldan/src/'):
        os.mkdir(f'./mockRepo/core-eldan/src/{job["Name"]}')
        copy_files(job_id, job["Name"])
    else:
        print(f"Folder for JobID: {job_id} ('{job['Name']}') already exists. Skipping...")
        

    # Mark current job as processed
    processed_jobs.add(job_id)

def copy_files(job_id, job_name):
    print(f"Copying files for JobID: {job_id} ('{job_name}') from the mockRepo/core-eldan/src/DataAccess folder...")
    os.system(f'cp -r ./mockRepo/core-eldan/src/DataAccess/* ./mockRepo/core-eldan/src/{job_name}/')
    # Replace DataAccess with job_name in the copied files
    os.system(f'find ./mockRepo/core-eldan/src/{job_name} -type f -exec sed -i "s/DataAccess/{job_name}/g" {{}} \;')
    print(f"Files copied and replaced for JobID: {job_id} ('{job_name}').")

# Main logic
def main():
    # Initialize gspread client and open spreadsheet
    gc = gspread.service_account(filename='./mockRepo/core-eldan/service-account.json')
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
