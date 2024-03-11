import json


def is_valid_json(json_str):
    """
    Check if the string is valid JSON and return the parsed JSON object if valid.
    """
    try:
        json_object = json.loads(json_str)
        return True, json_object
    except ValueError:
        return False, None

def flatten_message(entry):
    """
    Flatten the 'message' field of the entry, if it is a dictionary,
    into the parent dictionary with prefixed keys. If 'message' is a string
    or an integer, convert it into a dictionary with {"data": value}.
    """
    if 'message' in entry:
        if isinstance(entry['message'], dict):
            # If 'message' is a dictionary, proceed to flatten it
            for key, value in entry['message'].items():
                flat_key = f"message_{key}"
                entry[flat_key] = value
            del entry['message']
        elif isinstance(entry['message'], (str, int)):
            # If 'message' is a string or an int, wrap it in a dictionary
            entry['message'] = {"data": entry['message']}
        # Note: No need for an else block since we're now handling all cases
    return entry

# Path to your target.json file
file_path = 'target.json'

with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

transformed_data = []

for entry in data:
    # Check if 'message' is a string and a valid JSON
    if isinstance(entry['message'], str):
        is_valid, json_obj = is_valid_json(entry['message'].strip("'"))
        if is_valid:
            entry['message'] = json_obj  # Update 'message' with parsed JSON object
    # Flatten the entry including wrapping non-JSON message strings as {"data": value}
    flattened_entry = flatten_message(entry)
    transformed_data.append(flattened_entry)

# When writing the file, specify UTF-8 encoding
with open('targetlogs_flattened.json', 'w', encoding='utf-8') as file:
    for entry in transformed_data:
        json.dump(entry, file, ensure_ascii=False)
        file.write('\n')  # Write each entry on a new line

print("Transformation complete. Flattened data has been saved to 'targetlogs_flattened.json'.")
