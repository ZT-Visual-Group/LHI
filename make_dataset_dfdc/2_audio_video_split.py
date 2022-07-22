import os
import subprocess
import json
from make_dataset import dfdc_dataset_config as ddc

dfdc_data_real_path = ddc.dfdc_real_save_path
dfdc_data_fake_path = ddc.dfdc_fake_save_path
json_path = ddc.dfdc_work_dir+"/save.json"
save_path = ddc.dfdc_work_dir+"/ours/"

if not os.path.exists(save_path):
    os.makedirs(save_path)

lines = open(json_path, "r", encoding="utf-8")
sample = json.load(lines)

# #产生 1：1：1：1的真视频，假视频，真音频，假音频
for ori_name in sample.keys():
    if len(sample[ori_name]["fake_audio"]) > 0 and len(sample[ori_name]["fake_video"]) >0:
        ori_video_audio_path = dfdc_data_real_path + ori_name
        fake_video_path = dfdc_data_fake_path + sample[ori_name]["fake_video"][0]
        fake_audio_path = dfdc_data_fake_path + sample[ori_name]["fake_audio"][0]

        single_modal_file_path = os.path.join(save_path, ori_name)
        if not os.path.exists(single_modal_file_path):
            os.makedirs(single_modal_file_path)

        # 获取真音频
        command = ("ffmpeg -i %s -f wav -vn %s"%(ori_video_audio_path, single_modal_file_path+"/"+ori_name+"_0.wav"))
        output = subprocess.call(command, shell=True, stdout=None)

        # 获取真视频
        command = ("ffmpeg -i %s -vcodec copy -an %s" % (ori_video_audio_path, single_modal_file_path + "/" + ori_name + "_0.avi"))
        output = subprocess.call(command, shell=True, stdout=None)

        # 获取假视频
        command = ("ffmpeg -i %s -vcodec copy -an %s" % (fake_video_path, single_modal_file_path + "/" + ori_name + "_1.avi"))
        output = subprocess.call(command, shell=True, stdout=None)

        # 获取假音频
        command = ("ffmpeg -i %s -f wav -vn %s"%(fake_audio_path, single_modal_file_path+"/"+ori_name+"_1.wav"))
        output = subprocess.call(command, shell=True, stdout=None)

#
# count = 0
# for ori_name in sample.keys():
#     if len(sample[ori_name]["fake_audio"]) == 0 or len(sample[ori_name]["fake_video"]) ==0:
#         count+=1
#         if count > 5000:
#             break
#         ori_video_audio_path = dfdc_data_real_path + ori_name
#
#         single_modal_file_path = os.path.join(save_path, "00","00_"+ori_name)
#         if not os.path.exists(single_modal_file_path):
#             os.makedirs(single_modal_file_path)
#
#         # 获取真音频
#         command = ("ffmpeg -i %s -f wav -vn %s"%(ori_video_audio_path, single_modal_file_path+"/"+ori_name+"_0.wav"))
#         output = subprocess.call(command, shell=True, stdout=None)
#
#         # 获取真视频
#         command = ("ffmpeg -i %s -vcodec copy -an %s" % (ori_video_audio_path, single_modal_file_path + "/" + ori_name + "_0.avi"))
#         output = subprocess.call(command, shell=True, stdout=None)

