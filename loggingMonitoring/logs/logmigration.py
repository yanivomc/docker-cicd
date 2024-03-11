import json
import re

def try_fix_json(json_str):
    """
    Attempt to fix common issues in a stringified JSON.
    This function is basic and might not fix all problems.
    """
    try:
        # Attempt to fix common escaping issues and then load it as JSON
        fixed_str = json_str.replace("\\'", "'").replace('""', '"').replace("\'", "'")
        return json.loads(fixed_str)
    except json.JSONDecodeError:
        return None

# Path to your target.json file
file_path = 'target.json'

# Read the JSON data from the file
with open(file_path, 'r') as file:
    data = json.load(file)

# Initialize a list to hold the transformed (and valid) entries
transformed_data = []

for entry in data:
    message_str = entry['message'].strip("'")
    try:
        # Convert the stringified JSON message to a JSON object
        message_json = json.loads(message_str)
        entry['message'] = [message_json]  # Wrap the JSON object in a list, as per the requirement
        transformed_data.append(entry)
    except json.JSONDecodeError:
        # Attempt to fix and reparse the JSON string
        fixed_json = try_fix_json(message_str)
        if fixed_json:
            entry['message'] = [fixed_json]
            transformed_data.append(entry)
        else:
            # Log a message to the terminal if the entry is dropped
            print(f"Dropping entry due to invalid JSON in 'message' field. SessionID: {entry['SessionID']}")

# Write the valid and/or fixed data back to a new file
with open('targetlogs.json', 'w') as file:
    json.dump(transformed_data, file, indent=4)

print("Transformation complete. Valid data has been saved to 'targetlogs.json'.")
