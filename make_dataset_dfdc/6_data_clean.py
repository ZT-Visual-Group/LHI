import os
import shutil
from make_dataset import dfdc_dataset_config as ddc

dir_names = ["real_real", "real_fake", "fake_real", "fake_fake"]

def clean_short_sample(dir_name):
    path = ddc.dfdc_work_dir + "/dfdc_dataset/pycrop/" + dir_name + "/"
    for video_name in os.listdir(path):
        print(video_name)
        if len(os.listdir(os.path.join(path, video_name))) < 3:
            # print(video_name)
            shutil.rmtree(os.path.join(path, video_name))
            continue
        frames_path = os.path.join(path, video_name, "frames")
        if len(os.listdir(frames_path)) < 150:
            print(frames_path)
            shutil.rmtree(os.path.join(path, video_name))

for dir_name in dir_names:
    clean_short_sample(dir_name)