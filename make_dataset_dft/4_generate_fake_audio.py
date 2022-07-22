import os
import shutil
from make_dataset_dft import dataset_config

all_audio_names = []
# create full audio file dataset
crop_face_save_path = dataset_config.crop_face_save_path
if not os.path.exists(os.path.join(crop_face_save_path, "audio_tmp")):
    os.makedirs(os.path.join(crop_face_save_path, "audio_tmp"))
for dir_name in os.listdir(os.path.join(crop_face_save_path, "fake_real")):
    print(dir_name.split("-")[0])
    all_audio_names.append(dir_name.split("-")[0]+".wav")
    shutil.copy(os.path.join(crop_face_save_path, "fake_real", dir_name, "audio.wav"), os.path.join(crop_face_save_path, "audio_tmp", dir_name.split("-")[0]+".wav"))

# create fake_fake dir
if not os.path.exists(os.path.join(crop_face_save_path, "fake_fake")):
    os.makedirs(os.path.join(crop_face_save_path, "fake_fake"))
for dir_name in os.listdir(os.path.join(crop_face_save_path, "fake_real")):
    if not os.path.exists(os.path.join(crop_face_save_path, "fake_fake", dir_name)):
        os.makedirs(os.path.join(crop_face_save_path, "fake_fake", dir_name))
    # copy fake audio.wav
    wav_name = dir_name.split("-")[0]+".wav"
    for i in range(len(all_audio_names)):
        if wav_name != all_audio_names[i]:
            shutil.copy(os.path.join(crop_face_save_path, "audio_tmp", all_audio_names[i]), os.path.join(crop_face_save_path, "fake_fake", dir_name, "audio.wav"))
            break
    if not os.path.exists(os.path.join(crop_face_save_path, "fake_fake", dir_name, "frames")):
        os.makedirs(os.path.join(crop_face_save_path, "fake_fake", dir_name, "frames"))
    for img_name in os.listdir(os.path.join(crop_face_save_path, "fake_real", dir_name, "frames")):
        shutil.copy(os.path.join(crop_face_save_path, "fake_real", dir_name, "frames", img_name), os.path.join(crop_face_save_path, "fake_fake", dir_name, "frames", img_name))

# create real_fake dir
if not os.path.exists(os.path.join(crop_face_save_path, "real_fake")):
    os.makedirs(os.path.join(crop_face_save_path, "real_fake"))
for dir_name in os.listdir(os.path.join(crop_face_save_path, "real_real")):
    if not os.path.exists(os.path.join(crop_face_save_path, "real_fake", dir_name)):
        os.makedirs(os.path.join(crop_face_save_path, "real_fake", dir_name))
    # copy fake audio.wav
    wav_name = dir_name.split("-")[0]+".wav"
    for i in range(len(all_audio_names)):
        if wav_name != all_audio_names[i]:
            shutil.copy(os.path.join(crop_face_save_path, "audio_tmp", all_audio_names[i]), os.path.join(crop_face_save_path, "real_fake", dir_name, "audio.wav"))
            break
    if not os.path.exists(os.path.join(crop_face_save_path, "real_fake", dir_name, "frames")):
        os.makedirs(os.path.join(crop_face_save_path, "real_fake", dir_name, "frames"))
    for img_name in os.listdir(os.path.join(crop_face_save_path, "real_real", dir_name, "frames")):
        shutil.copy(os.path.join(crop_face_save_path, "real_real", dir_name, "frames", img_name), os.path.join(crop_face_save_path, "real_fake", dir_name, "frames", img_name))



