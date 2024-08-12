import json
import random
import datetime
from time import sleep
import uuid
from faker import Faker

# Initialize Faker
fake = Faker()

# Arrays for random selection
application_names = ["App1", "App2", "App3", "App4", "App5"]
error_levels = ["Error", "Warning", "Info"]
error_types = [
	"System.Exception", "System.NullReferenceException", "System.IndexOutOfRangeException",
	"System.InvalidOperationException", "System.ArgumentException", "System.ArgumentNullException",
	"System.ArgumentOutOfRangeException", "System.IO.IOException", "System.NotImplementedException",
	"System.NotSupportedException", "System.TimeoutException", "System.UnauthorizedAccessException",
	"System.FormatException", "System.OverflowException", "System.OutOfMemoryException",
	"System.StackOverflowException", "System.TypeInitializationException", "System.InvalidCastException",
	"System.InvalidProgramException", "System.MemberAccessException"
]
system_names = ["System1", "System2", "System3", "System4", "System5"]
machine_names = ["Machine1", "Machine2", "Machine3", "Machine4", "Machine5"]
environment_names = ["Production", "Staging", "QA1", "QA2", "QA3"]
user_names = ["user1", "user2", "user3", "user4", "user5", "user6", "user7", "user8", "user9", "user10"]

def generate_log_entry():
	log_entry = {
		"log_id": str(uuid.uuid4()),
		"timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
		"severity": random.choice(error_levels),
		"error_type": random.choice(error_types),
		"error_message": fake.sentence(nb_words=6),
		"stack_trace": fake.text(max_nb_chars=200),
		"loggerSessionID": str(uuid.uuid4()),
		"systemName": random.choice(system_names),
		"environmentName": random.choice(environment_names),
		"applicationName": random.choice(application_names),
		"eventID": "ID" + str(random.randint(100, 999)),
		"machineName": random.choice(machine_names),
		"userName": random.choice(user_names)
	}
	return log_entry

def generate_logs_to_file(file_path, num_logs):
	with open(file_path, 'w') as file:
		logs = [generate_log_entry() for _ in range(num_logs)]
		json.dump(logs, file, indent=4)

# Generate 10 logs and write to 'logs.json'
while True:
    generate_logs_to_file('logs.json', 10)
    sleep(1)
	