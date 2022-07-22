import json
import os
from make_dataset import dfdc_dataset_config as ddc

real_fake_group = {}
fakes = []
save_all_path = ddc.dfdc_work_dir+"/save_all.json"
real_fake_group_save_path = ddc.dfdc_work_dir+"/save.json"

if os.path.exists(save_all_path):
    os.remove(save_all_path)
if os.path.exists(real_fake_group_save_path):
    os.remove(real_fake_group_save_path)

# merge all json files to json_all.json
save_dict = {}
save_merge = open(save_all_path, "a", encoding="utf-8")
json_path = os.path.abspath(".")+"/json_files"
for dir_name in os.listdir(json_path):
    single_json = open(json_path+"/"+dir_name, "r")
    single_json = json.load(single_json)
    for name in sorted(single_json.keys()):
        save_dict[name] = single_json[name]

print("All json files merge finish!")
json.dump(save_dict, save_merge, ensure_ascii=False)
save_merge.close()

# generate all fake audio array
csv_data = open(ddc.dfdc_work_dir+"/metadata_fake_audio.csv", "r")
csv_lines = csv_data.readlines()
fake_audios = [line.split()[0] for line in csv_lines]
print("Fake_audios array generate finish!")

save = open(real_fake_group_save_path, "a", encoding="utf8")
with open(save_all_path, "r") as a:
    json_data = json.load(a)
    # print("json_data", sorted(json_data.keys()))
    for name in sorted(json_data.keys()):
        if json_data[name]["label"] == "FAKE":
            real_fake_group[json_data[name]["original"]] = {}
            real_fake_group[json_data[name]["original"]]["fake_video"] = []
            real_fake_group[json_data[name]["original"]]["fake_audio"] = []

            # print(real_fake_group)
    for name in sorted(json_data.keys()):
        if json_data[name]["label"] == "FAKE":
            if name not in fake_audios:
                group = real_fake_group[json_data[name]["original"]]["fake_video"]
                if name not in group:
                    group.append(name)
                real_fake_group[json_data[name]["original"]]["fake_video"] = group
            else:
                group_fake_audio = real_fake_group[json_data[name]["original"]]["fake_audio"]
                if name not in group_fake_audio:
                    group_fake_audio.append(name)
                real_fake_group[json_data[name]["original"]]["fake_audio"] = group_fake_audio
    json.dump(real_fake_group, save)
    print(real_fake_group["xugmhbetrw.mp4"])

