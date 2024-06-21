import json
import os
import matplotlib.pyplot as plt
import mplcyberpunk

INSTAGRAM_DM_FOLDER = "A:\\InstaDiscord Packages\\Insta Packages\\Raj\\instagram-yourfavraj-2024-06-21-2vougal2\\your_instagram_activity\\messages\\inbox\\devanshi_17968828766664318"

from datetime import datetime, timedelta
import pytz


def create_date_dict(starting_epoch, ending_epoch, timezone='Asia/Qatar'):
    # Convert epoch to datetime objects in the specified timezone
    tz = pytz.timezone(timezone)

    # Convert epoch to datetime objects in the specified timezone
    try:
        start_date = datetime.fromtimestamp(starting_epoch, tz)
        end_date = datetime.fromtimestamp(ending_epoch, tz)
    except (OverflowError, OSError) as e:
        raise ValueError(f"Invalid epoch time: {e}")

    # Initialize the result dictionary
    date_dict = {}

    # Generate the range of dates
    current_date = start_date
    while current_date <= end_date:
        # Format the date as "dd/mm/yy"
        date_str = current_date.strftime("%d/%m/%y")
        # Initialize with value 0
        date_dict[date_str] = 0
        # Move to the next day
        current_date += timedelta(days=1)

    return date_dict

# {instagram-data-folder}/your_instagram_activity/messages/inbox/{dm}
# The folder of your DMs with them


class User:
    def __init__(self, sender):
        self.sender = sender
        self.messages: list = []


user_1 = None
user_2 = None
users = []

# Load all messages into memory
for item in os.listdir(INSTAGRAM_DM_FOLDER):

    # Ignore files/folders we don't care about
    if not item.endswith(".json"):
        continue
    elif not item.startswith("message_"):
        continue

    # Go through the messages files
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

print("Total no of messages: ", (len(combined_messages)))

plt.style.use("cyberpunk")
plt.xticks(rotation=90)

# Graph: Messages per day
date_dict = create_date_dict(combined_messages[0]['timestamp'], combined_messages[-1]['timestamp'])

for message in combined_messages:
    date_dict[datetime.fromtimestamp(message['timestamp']).strftime("%d/%m/%y")] += 1

dpi = 96

# plt.rcParams['figure.figsize'] = [
#         len(list(date_dict.values())) / dpi, # width
#         len(date_dict.keys()) / 10 * dpi   # Height
#     ]
plt.figure(figsize=(71.95, 38.41), dpi=100)


plt.plot(list(date_dict.keys()), list(date_dict.values()))


mplcyberpunk.make_lines_glow()
mplcyberpunk.add_underglow()

plt.savefig('./myfig.png', dpi=100)
