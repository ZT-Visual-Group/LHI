import glob
import json
import os
import subprocess
import librosa
import numpy as np
import tqdm
from make_dataset import dfdc_dataset_config as ddc

dfdc_train_wav_path_fake = ddc.dfdc_fake_save_path
dfdc_train_wav_path_real = ddc.dfdc_real_save_path
altered_audio_path = ddc.dfdc_work_dir + "/wav/"
fake_audio_save_path = ddc.dfdc_work_dir + "/metadata_fake_audio.csv"
metadata_all_path = os.path.abspath(".")+"/json_files/"

def audio_altered(fake_path, fake_video, orig_path, orig_video):

    """Finds out if audio of fake_video was altered.

    # Arguments
        fake_path: fake mp4 video path name
        fake_video: fake mp4 video name
        orig_path: original mp4 video path name
        orig_video: original mp4 video name

    # Returns
        True - if audio of fake mp4 video was altered
        False - otherwise
    """

    fake_wav = fake_video[:-4] + '.wav'
    fake_wav_path = altered_audio_path + fake_wav
    fake_path = fake_path + fake_video
    # print(fake_path)
    try:
        # in case if .wav has already been extracted
        fake_data, fake_rate = librosa.load(fake_wav_path, sr=None)
    except FileNotFoundError:
        # extract fake_path audio
        # .wav audio format is used because librosa.load() doesn't work with .aac
        command = "ffmpeg -i %s -vn -f wav %s" % (fake_path, fake_wav_path)
        subprocess.run(command, shell=True)

        try:
            fake_data, fake_rate = librosa.load(fake_wav_path, sr=None)
        except FileNotFoundError:
            # if fake video has no audio than its audio is not altered
            return False

    orig_wav = orig_video[:-4] + '.wav'
    orig_wav_path = altered_audio_path + orig_wav
    orig_path = orig_path + orig_video
    # print(orig_path)
    try:
        # in case if .wav has already been extracted
        orig_data, orig_rate = librosa.load(orig_wav_path, sr=None)
    except FileNotFoundError:
        # extract orig_path audio
        # .wav audio format is used because librosa.load() doesn't work with .aac
        command = "ffmpeg -i %s -vn -f wav %s" % (orig_path, orig_wav_path)
        subprocess.run(command, shell=True)

        try:
            orig_data, orig_rate = librosa.load(orig_wav_path, sr=None)
        except FileNotFoundError:
            # if original video has no audio but fake video does than audio is altered
            return True
    # print(fake_rate, orig_rate)
    return fake_rate != orig_rate or not np.array_equal(fake_data, orig_data)


def main(json_path):
    """
    json_path: path to all metadata.json
    the dir structure is just like: ./make_dataset/json_files/metadata*.json
    """
    json_data = open(json_path, "r")
    json_data = json.load(json_data)
    fake_save = open(fake_audio_save_path, "a+")
    for name in tqdm.tqdm(sorted(json_data.keys())):
        # print(name)
        if json_data[name]["label"] == "FAKE":
            fake_name = name
            real_name = json_data[name]["original"]
            # print(fake_name + " " + real_name)
            flag = audio_altered(dfdc_train_wav_path_fake, fake_name, dfdc_train_wav_path_real, real_name)
            if flag == True:
                    print(fake_name+" "+real_name)
                    fake_save.write(fake_name+" "+real_name+"\n")

if __name__ == '__main__':
    if not os.path.exists(altered_audio_path):
        os.mkdir(altered_audio_path)
    for metadata_path in sorted(os.listdir(metadata_all_path)):
        main(json_path=metadata_all_path+metadata_path)
