import os
import shutil
from make_dataset_dft import dataset_config

dir_names = ["real_real", "real_fake", "fake_real", "fake_fake"]

for dir_name in dir_names:
    path = dataset_config.crop_face_save_path + dir_name
    print("Clean %s"% dir_name)
    for video_name in os.listdir(path):
        frames_path = os.path.join(path, video_name, "frames")
        if len(os.listdir(frames_path)) < 60:
            print(frames_path)
            shutil.rmtree(os.path.join(path, video_name))

