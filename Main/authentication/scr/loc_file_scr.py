import json

from Main.assets.loc_file_path import assert_loc_path

with open(assert_loc_path + r"\messages\unsupported_message.txt", "r") as file:
    unsupported_message_contents = file.read()
    file.close()

with open(assert_loc_path + r"\messages\registration_text.txt", "r") as file1:
    registration_text_data = file1.read()
    file1.close()

read_app_data = open(assert_loc_path + r"\data\app_data.json")
app_data: dict = json.load(read_app_data)
read_app_data.close()

file0 = open(assert_loc_path + r"\messages\message.json")
messages: dict = json.load(file0)
file0.close()

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

read_message_data = open(assert_loc_path + r"\messages\warning.json")
warnings: dict = json.load(read_message_data)
read_message_data.close()

f3_1 = open(assert_loc_path + r"\messages\error.json")
error_data: dict = json.load(f3_1)
f3_1.close()


