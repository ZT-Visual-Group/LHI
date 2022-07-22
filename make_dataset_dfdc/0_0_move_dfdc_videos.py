import os
import json
import shutil
from make_dataset import dfdc_dataset_config as ddc

# DFDC path: "/home/zbp/Data/DFDC"

dfdc_save_path = ddc.dfdc_save_path
if not os.path.exists(ddc.dfdc_fake_save_path):
    os.mkdir(ddc.dfdc_fake_save_path)
if not os.path.exists(ddc.dfdc_real_save_path):
    os.mkdir(ddc.dfdc_real_save_path)

for dir_name in os.listdir(dfdc_save_path):
    if dir_name.startswith("dfdc_train_part") and not dir_name.endswith("zip"):
        meta_json_path = os.path.join(dfdc_save_path, dir_name, "metadata.json")
        label_single_json = open(meta_json_path, "r")
        label_path = json.load(label_single_json)
        for vid_name in sorted(label_path.keys()):
            if label_path[vid_name]["label"] == "FAKE":
                print("Fake Name",vid_name)
                shutil.copy(os.path.join(dfdc_save_path, dir_name, vid_name), os.path.join(ddc.dfdc_fake_save_path, vid_name))
            else:
                print("Real Name",vid_name)
                shutil.copy(os.path.join(dfdc_save_path, dir_name, vid_name),
                          os.path.join(ddc.dfdc_real_save_path, vid_name))





