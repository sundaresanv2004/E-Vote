import json

from Main.assets.loc_file_path import local_assets_path

with open(local_assets_path + r"\data\app_data.json", 'r') as f:
    app_data: dict = json.load(f)
    f.close()

with open(local_assets_path + r"\messages\message.json", 'r') as f:
    messages: dict = json.load(f)
    f.close()

read_file_data = open(local_assets_path + r"\data\file_data.json")
file_data: dict = json.load(read_file_data)
read_file_data.close()

read_settings_file = open(local_assets_path + r"\data\default_setting.json")
default_setting_data: dict = json.load(read_settings_file)
read_settings_file.close()

read_election_setting = open(local_assets_path + r"\data\default_election_settings.json")
default_election_setting_data: dict = json.load(read_election_setting)
read_election_setting.close()

read_file_path = open(local_assets_path + r"\data\file_path.json")
file_path: dict = json.load(read_file_path)
read_file_path.close()

read_message_data = open(local_assets_path + r"\messages\warning.json")
warnings: dict = json.load(read_message_data)
read_message_data.close()

f3_1 = open(local_assets_path + r"\messages\error.json")
error_data: dict = json.load(f3_1)
f3_1.close()

with open(local_assets_path + r'\messages\all_done.txt', 'r') as f:
    all_done_message = f.read()
    f.close()
