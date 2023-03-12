import json

from Main.assets.loc_file_path import assert_loc_path

read_app_data = open(assert_loc_path + r"\data\app_data.json")
app_data: dict = json.load(read_app_data)
read_app_data.close()

read_file_data = open(assert_loc_path + r"\data\file_data.json")
file_data: dict = json.load(read_file_data)
read_file_data.close()

read_settings_file = open(assert_loc_path + r"\data\default_setting.json")
default_setting_data: dict = json.load(read_settings_file)
read_settings_file.close()

read_election_setting = open(assert_loc_path + r"\data\default_election_settings.json")
default_election_setting_data: dict = json.load(read_election_setting)
read_election_setting.close()

read_file_path = open(assert_loc_path + r"\data\file_path.json")
file_path: dict = json.load(read_file_path)
read_file_path.close()

read_message_data = open(assert_loc_path + r"\messages\message.json")
message_data: dict = json.load(read_message_data)
read_message_data.close()
