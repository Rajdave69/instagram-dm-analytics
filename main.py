import json
import os
import matplotlib.pyplot as plt
import mplcyberpunk
from datetime import datetime, timedelta
import pytz


# Define the function to create a dictionary of dates
def create_date_dict(starting_epoch, ending_epoch, timezone='Asia/Qatar'):
    tz = pytz.timezone(timezone)
    try:
        start_date = datetime.fromtimestamp(starting_epoch, tz)
        end_date = datetime.fromtimestamp(ending_epoch, tz)
    except (OverflowError, OSError) as e:
        raise ValueError(f"Invalid epoch time: {e}")

    date_dict = {}
    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.strftime("%d/%m/%y")
        date_dict[date_str] = 0
        current_date += timedelta(days=1)

    return date_dict


# Define the User class to hold messages
class User:
    def __init__(self, sender):
        self.sender = sender
        self.messages = []


# Load messages from JSON files
INSTAGRAM_DM_FOLDER = "A:\\InstaDiscord Packages\\Insta Packages\\Raj\\instagram-yourfavraj-2024-06-21-2vougal2\\your_instagram_activity\\messages\\inbox\\alinyay_17973979022664318"

user_1 = None
user_2 = None
users = []

for item in os.listdir(INSTAGRAM_DM_FOLDER):
    if not item.endswith(".json") or not item.startswith("message_"):
        continue

    file_data = json.load(open(f"{INSTAGRAM_DM_FOLDER}//{item}"))

    if user_1 is None or user_2 is None:
        user_1 = User(file_data['participants'][0]['name'])
        user_2 = User(file_data['participants'][1]['name'])
        users = {
            file_data['participants'][0]['name']: user_1,
            file_data['participants'][1]['name']: user_2,
        }

    for message in file_data['messages']:
        users[message['sender_name']].messages.append({
            'sender_name': message['sender_name'],
            'timestamp': message['timestamp_ms'] / 1000,
            'content': message.get('content')
        })

combined_messages = [*user_1.messages, *user_2.messages]
combined_messages.sort(key=lambda thing: thing['timestamp'])

print("Total no of messages: ", len(combined_messages))
print(f"Messages sent by {user_1.sender}: {len(user_1.messages)}")
print(f"Messages sent by {user_2.sender}: {len(user_2.messages)}")

# Create the date dictionary for plotting
start_epoch = combined_messages[0]['timestamp']
end_epoch = combined_messages[-1]['timestamp']
date_dict = create_date_dict(start_epoch, end_epoch)

# Populate the date dictionary with message counts
for message in combined_messages:
    date_key = datetime.fromtimestamp(message['timestamp']).strftime("%d/%m/%y")
    date_dict[date_key] += 1


# Calculate message lengths for each user, ignoring messages with None or empty content
def calculate_average_length(messages):
    valid_messages = [msg for msg in messages if msg['content'] is not None and msg['content'].strip()]
    total_length = sum(len(msg['content']) for msg in valid_messages)
    total_messages = len(valid_messages)
    return total_length / total_messages if total_messages > 0 else 0


average_length_user1 = calculate_average_length(user_1.messages)
average_length_user2 = calculate_average_length(user_2.messages)
net_average_length = calculate_average_length(combined_messages)

print(f"Net Average Message Length: {net_average_length:.2f}")
print(f"Average Message Length for {user_1.sender}: {average_length_user1:.2f}")
print(f"Average Message Length for {user_2.sender}: {average_length_user2:.2f}")

# Plot the overall message data
plt.style.use("cyberpunk")
x_labels = list(date_dict.keys())
y_values = list(date_dict.values())

# Set a fixed height and dynamic width for a landscape orientation
fig_width = max(20, len(x_labels) // 4)  # Ensure a minimum width
fig_height = 10  # Fixed height for landscape orientation
plt.figure(figsize=(fig_width, fig_height), dpi=100)

plt.plot(x_labels, y_values, marker='o', label="Total Messages")

# Format the x-axis and y-axis
plt.xticks(rotation=90, fontsize=14, ha='center')  # Rotate and set font size for x-axis labels
plt.yticks(fontsize=32)  # Increase font size for y-axis labels
plt.xlabel("Date", fontsize=36)
plt.ylabel("Number of Messages", fontsize=36)
plt.title("Total Messages Per Day", fontsize=40)
plt.grid(visible=True, linestyle='--', alpha=0.7)
plt.legend(fontsize=20)

# Remove excess empty space around the plot
plt.tight_layout()

# Add cyberpunk effects
mplcyberpunk.make_lines_glow()
mplcyberpunk.add_underglow()

# Save the overall message plot to a file
plt.savefig('./total_messages.png', dpi=100)
plt.show()

# Create separate date dictionaries for each user
date_dict_user1 = create_date_dict(start_epoch, end_epoch)
date_dict_user2 = create_date_dict(start_epoch, end_epoch)

# Populate the user-specific date dictionaries
for message in combined_messages:
    date_key = datetime.fromtimestamp(message['timestamp']).strftime("%d/%m/%y")
    if message['sender_name'] == user_1.sender:
        date_dict_user1[date_key] += 1
    elif message['sender_name'] == user_2.sender:
        date_dict_user2[date_key] += 1

# Plot the user-specific message data
plt.figure(figsize=(fig_width, fig_height), dpi=100)

plt.plot(x_labels, list(date_dict_user1.values()), marker='o', label=user_1.sender)
plt.plot(x_labels, list(date_dict_user2.values()), marker='s', label=user_2.sender)

# Format the x-axis and y-axis
plt.xticks(rotation=90, fontsize=14, ha='center')  # Rotate and set font size for x-axis labels
plt.yticks(fontsize=32)  # Increase font size for y-axis labels
plt.xlabel("Date", fontsize=36)
plt.ylabel("Number of Messages", fontsize=36)
plt.title("Messages Per Day by User", fontsize=40)
plt.grid(visible=True, linestyle='--', alpha=0.7)
plt.legend(fontsize=20)

# Remove excess empty space around the plot
plt.tight_layout()

# Add cyberpunk effects
mplcyberpunk.make_lines_glow()
mplcyberpunk.add_underglow()

# Save the user-specific message plot to a file
plt.savefig('./user_specific_messages.png', dpi=100)
plt.show()

# Calculate messages per hour
hour_dict = {hour: 0 for hour in range(24)}

for message in combined_messages:
    hour = datetime.fromtimestamp(message['timestamp']).hour
    hour_dict[hour] += 1

# Plot the messages per hour
hours = list(hour_dict.keys())
messages_per_hour = list(hour_dict.values())

plt.figure(figsize=(16, 10), dpi=100)

bars = plt.bar(hours, messages_per_hour, color='cyan', edgecolor='black')
mplcyberpunk.add_bar_gradient(bars=bars)

# Format the x-axis and y-axis
plt.xticks(hours, fontsize=18)  # Set font size for x-axis labels (0-23)
plt.yticks(fontsize=32)  # Increase font size for y-axis labels
plt.xlabel("Hour of Day (0-23)", fontsize=36)
plt.ylabel("Number of Messages", fontsize=36)
plt.title("Messages Distribution by Hour of Day", fontsize=40)
plt.grid(visible=True, linestyle='--', alpha=0.7)

# Remove excess empty space around the plot
plt.tight_layout()

# Save the hourly distribution plot to a file
plt.savefig('./hourly_distribution.png', dpi=100)
plt.show()
