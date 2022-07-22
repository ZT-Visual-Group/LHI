import os
import subprocess
import json
import shutil
from make_dataset_dft import dataset_config

timit_fake_data_path = dataset_config.timit_fake_path
save_path = dataset_config.timit_fake_save_path

for dir_name in os.listdir(timit_fake_data_path):
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    if "dircksum" in dir_name:
        continue
    video_path = os.path.join(timit_fake_data_path, dir_name)
    for video_name in os.listdir(video_path):
        if video_name.endswith("avi"):
            video_name1 = video_name.replace("video", dir_name)
            print(os.path.join(video_path, video_name), save_path+"/"+video_name1)
            shutil.copy(os.path.join(video_path, video_name), save_path+"/"+video_name1)