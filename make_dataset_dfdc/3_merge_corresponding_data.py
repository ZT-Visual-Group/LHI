import os
import subprocess
from make_dataset import dfdc_dataset_config as ddc

single_modal_save_path = ddc.dfdc_work_dir +"/ours"
dir_names = os.listdir(single_modal_save_path)
for dir_name in dir_names:
    if dir_name != "00":
        # pass
        # print(dir_name)
        video_audio_path = os.path.join(single_modal_save_path, dir_name)
        real_video_name = os.path.join(video_audio_path, dir_name+"_0.avi")
        real_audio_name = os.path.join(video_audio_path, dir_name+"_0.wav")
        fake_video_name = os.path.join(video_audio_path, dir_name+"_1.avi")
        fake_audio_name = os.path.join(video_audio_path, dir_name+"_1.wav")

        # 视频音频对保存路径
        real_real_save_path = os.path.join(video_audio_path, "00_" + dir_name + ".avi")
        real_fake_save_path = os.path.join(video_audio_path, "01_" + dir_name + ".avi")
        fake_real_save_path = os.path.join(video_audio_path, "10_" + dir_name + ".avi")
        fake_fake_save_path = os.path.join(video_audio_path, "11_" + dir_name + ".avi")
        # 生成真真-视频音频对 00-文件名
        command = ("ffmpeg -i %s -i %s -c:v copy -c:a aac -strict experimental %s"%(real_video_name, real_audio_name, real_real_save_path))
        output = subprocess.call(command, shell=True, stdout=None)
        # 生成真假-视频音频对 01-文件名
        command = ("ffmpeg -i %s -i %s -c:v copy -c:a aac -strict experimental %s"%(real_video_name, fake_audio_name, real_fake_save_path))
        output = subprocess.call(command, shell=True, stdout=None)
        # 生成假真-视频音频对 10-文件名
        command = ("ffmpeg -i %s -i %s -c:v copy -c:a aac -strict experimental %s"%(fake_video_name, real_audio_name, fake_real_save_path))
        output = subprocess.call(command, shell=True, stdout=None)
        # 生成假假-视频音频对 11-文件名
        command = ("ffmpeg -i %s -i %s -c:v copy -c:a aac -strict experimental %s"%(fake_video_name, fake_audio_name, fake_fake_save_path))
        output = subprocess.call(command, shell=True, stdout=None)
    elif dir_name == "00":
        pass
        # video_audio_path = os.path.join(single_modal_save_path, dir_name)
        # for video_name in os.listdir(video_audio_path):
        #     print(video_name)
        #     real_add_video_name = os.path.join(video_audio_path, video_name, video_name.split("_")[1]+"_0.avi")
        #     real_add_audio_name = os.path.join(video_audio_path, video_name, video_name.split("_")[1]+"_0.wav")
        #
        #     # 视频音频对保存路径
        #     real_real_add_save_path = os.path.join(video_audio_path, video_name, "00_" + video_name.split("_")[1] + ".avi")
        #
        #     # 生成真真-视频音频对 00-文件名
        #     command = ("ffmpeg -i %s -i %s -c:v copy -c:a aac -strict experimental %s"%(real_add_video_name, real_add_audio_name, real_real_add_save_path))
        #     output = subprocess.call(command, shell=True, stdout=None)


