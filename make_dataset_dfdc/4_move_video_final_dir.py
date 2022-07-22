import os
import shutil
import tqdm
from make_dataset import dfdc_dataset_config as ddc

dir_path = ddc.dfdc_work_dir + "/ours"
final_path = ddc.dfdc_work_dir + "/dfdc_dataset"

if not os.path.exists(final_path):
    os.makedirs(final_path+"/real_real")
    os.makedirs(final_path + "/real_fake")
    os.makedirs(final_path + "/fake_real")
    os.makedirs(final_path + "/fake_fake")

for dir_name in tqdm.tqdm(os.listdir(dir_path)):
    if dir_name != "00":
        video_audio_path = os.path.join(dir_path, dir_name)
        real_real_ori_path = os.path.join(video_audio_path, "00_"+dir_name+".avi")
        real_fake_ori_path = os.path.join(video_audio_path, "01_" + dir_name + ".avi")
        fake_real_ori_path = os.path.join(video_audio_path, "10_" + dir_name + ".avi")
        fake_fake_ori_path = os.path.join(video_audio_path, "11_" + dir_name + ".avi")

        real_real_final_path = os.path.join(final_path, "real_real","00_" + dir_name + ".avi")
        real_fake_final_path = os.path.join(final_path, "real_fake", "01_" + dir_name + ".avi")
        fake_real_final_path = os.path.join(final_path, "fake_real", "10_" + dir_name + ".avi")
        fake_fake_final_path = os.path.join(final_path, "fake_fake", "11_" + dir_name + ".avi")

        shutil.copy(real_real_ori_path, real_real_final_path)
        shutil.copy(real_fake_ori_path, real_fake_final_path)
        shutil.copy(fake_real_ori_path, fake_real_final_path)
        shutil.copy(fake_fake_ori_path, fake_fake_final_path)

    elif dir_name == "00":
        # for video_name in tqdm.tqdm(os.listdir(os.path.join(dir_path, dir_name))):
        #     video_audio_path = os.path.join(dir_path, dir_name)
        #     real_real_add_ori_path = os.path.join(video_audio_path, video_name, video_name+".avi")
        #     real_real_add_final_path = os.path.join(final_path, "real_real_add", video_name + ".avi")
        #     # print(real_real_add_ori_path, "\n",real_real_add_final_path)
        #     shutil.copy(real_real_add_ori_path, real_real_add_final_path)
        pass


