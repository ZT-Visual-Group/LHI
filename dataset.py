from torch.utils.data import Dataset
from PIL import Image
import torch
import os
import librosa
from audio_utils.utils_audio import *
import config
import torchvision.transforms as transforms
import numpy as np
from sklearn import preprocessing

def readTxt(file_path):
    img_list = []
    with open(file_path, 'r') as file_to_read:
        while True:
            lines = file_to_read.readline()
            if not lines:
                break
            item = lines.strip().split()
            img_list.append(item)
    file_to_read.close()
    return img_list

def readTxt_audio(file_path):
    img_list = []
    with open(file_path, 'r') as file_to_read:
        while True:
            lines = file_to_read.readline()
            if not lines:
                break
            item = lines.strip().split(",")
            img_list.append(item)
    file_to_read.close()
    return img_list

class RoadSequenceDataset(Dataset):
    def __init__(self, file_path, transforms):
        self.img_list = readTxt(file_path)
        self.dataset_size = len(self.img_list)
        self.transforms = transforms
    def __len__(self):
        return self.dataset_size
    def __getitem__(self, idx):
        img_path_list = self.img_list[idx]
        if img_path_list[1] == "fake" and img_path_list[2] == "fake":
            path = config.multi_modal_dataset_save_path+"fake_fake/"
        elif img_path_list[1] == "real" and img_path_list[2] == "fake":
            path = config.multi_modal_dataset_save_path+"real_fake/"
        elif img_path_list[1] == "fake" and img_path_list[2] == "real":
            path = config.multi_modal_dataset_save_path+"fake_real/"
        elif img_path_list[1] == "real" and img_path_list[2] == "real":
            path = config.multi_modal_dataset_save_path+"real_real/"

        data = self.transforms(Image.open(path + img_path_list[0]+"/frames/%06d.jpg"%1))
        flag = img_path_list[1]
        label = 0.5
        if flag == "fake":
            label = 1
        elif flag == "real":
            label = 0
        sample = {'data': data, 'data_2d': data,'label': label}
        return sample

class RoadAudioDataset(Dataset):
    def __init__(self, file_path, transforms):
        self.img_list = readTxt(file_path)
        self.dataset_size = len(self.img_list)
        self.transforms = transforms
        self.SAMPLE_RATE = 32000
        self.SPEC_HEIGHT = 200
        self.SPEC_WIDTH = 400
        self.FMIN = 5
        self.FMAX = 15000
        self.size = 5
        self.max_file = 538

    def __len__(self):
        return self.dataset_size

    def __getitem__(self, idx):
        img_path_list = self.img_list[idx]
        if img_path_list[1] == "fake" and img_path_list[2] == "fake":
            path = config.multi_modal_dataset_save_path+"fake_fake/"
        elif img_path_list[1] == "real" and img_path_list[2] == "fake":
            path = config.multi_modal_dataset_save_path+"real_fake/"
        elif img_path_list[1] == "fake" and img_path_list[2] == "real":
            path = config.multi_modal_dataset_save_path+"fake_real/"
        elif img_path_list[1] == "real" and img_path_list[2] == "real":
            path = config.multi_modal_dataset_save_path+"real_real/"


        fn = os.path.join(path + img_path_list[0] + "/audio.wav")
        X, sample_rate = librosa.load(fn, 32000, res_type='kaiser_fast')
        X_log_mel, width = extract_logmel(X, sample_rate, self.size, self.SPEC_HEIGHT, self.SPEC_WIDTH, self.FMIN,
                                          self.FMAX)
        X_log_mel = np.array(X_log_mel)
        flag = img_path_list[2]
        label = 0.5
        if flag == "fake":
            label = 1
        elif flag == "real":
            label = 0
        sample = {'data': X_log_mel, 'data_2d': X_log_mel, 'label': label}
        return sample

class RoadSequenceDatasetList(Dataset):
    def __init__(self, file_path, transforms, transforms_2d):
        self.img_list = readTxt(file_path)
        self.dataset_size = len(self.img_list)
        self.transforms = transforms
        self.transforms_2d = transforms_2d
        self.SAMPLE_RATE = 32000
        self.SPEC_HEIGHT = 200
        self.SPEC_WIDTH = 320
        self.FMIN = 5
        self.FMAX = 15000
        self.size = 5
        self.max_file = 538
    def __len__(self):
        return self.dataset_size
    def __getitem__(self, idx):
        img_path_list = self.img_list[idx]
        data, data_2d, label = [], [], 0.5

        if img_path_list[1] == "fake" and img_path_list[2] == "fake":
            path = config.multi_modal_dataset_save_path+"fake_fake/"
        elif img_path_list[1] == "real" and img_path_list[2] == "fake":
            path = config.multi_modal_dataset_save_path+"real_fake/"
        elif img_path_list[1] == "fake" and img_path_list[2] == "real":
            path = config.multi_modal_dataset_save_path+"fake_real/"
        elif img_path_list[1] == "real" and img_path_list[2] == "real":
            path = config.multi_modal_dataset_save_path+"real_real/"

        for i in range(1, 60, 2):
            data.append(torch.unsqueeze(self.transforms(Image.open(path + img_path_list[0]+"/frames/%06d.jpg"%i)), dim=0))
            if i < 10:
                data_2d.append(torch.unsqueeze(self.transforms(Image.open(path + img_path_list[0]+"/frames/%06d.jpg"%i)), dim=0))
        data = torch.cat(data, 0)
        data = data.transpose(1, 0)
        data_2d = torch.cat(data_2d, 0)
        fn = os.path.join(path + img_path_list[0] + "/audio.wav")
        X, sample_rate = librosa.load(fn, 32000, res_type='kaiser_fast')
        X_log_mel, width = extract_logmel(X, sample_rate, self.size, self.SPEC_HEIGHT, self.SPEC_WIDTH, self.FMIN,
                                          self.FMAX)
        X_log_mel = np.array(X_log_mel)
        flag = img_path_list[3]

        label = 0.5
        if flag == "fake":
            label = 1
        elif flag == "real":
            label = 0
        sample = {'data': data, "data_2d": data_2d, "data_aud": X_log_mel,'label': label}
        return sample

