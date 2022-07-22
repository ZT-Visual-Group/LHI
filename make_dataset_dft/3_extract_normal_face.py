import argparse, imageio, subprocess, os, cv2
from shutil import rmtree
import shutil
import tqdm
from make_dataset_dft.run_pipeline import *
from make_dataset_dft import dataset_config

parser = argparse.ArgumentParser(description = "PreProcess")
parser.add_argument('--out_dir',type=str, default= dataset_config.crop_face_out_path, help='Output direcotry')
opt = parser.parse_args()

setattr(opt,'data_dir',os.path.join(opt.out_dir))
setattr(opt,'fake_dir',os.path.join(opt.data_dir,'fake_real'))
setattr(opt,'real_dir',os.path.join(opt.data_dir,'real_real'))

if not os.path.exists(os.path.join(opt.data_dir,'pycrop')):
    os.makedirs(os.path.join(opt.data_dir,'pycrop'))

if not os.path.exists(os.path.join(opt.data_dir,'pytmp')):
    os.makedirs(os.path.join(opt.data_dir,'pytmp'))

setattr(opt,'tmp_dir',os.path.join(opt.data_dir,'pytmp'))
setattr(opt,'crop_dir',os.path.join(opt.data_dir,'pycrop'))

for video in tqdm.tqdm(os.listdir(opt.fake_dir)):
	if not os.path.exists(os.path.join(opt.data_dir,'pycrop','fake_real',os.path.basename(video)[0:-4])):
		print(video)
		run_pipeline(opt.data_dir,os.path.join(opt.fake_dir,video),os.path.basename(video)[0:-4],'fake_real')

for directory in os.listdir(os.path.join(opt.crop_dir,'fake_real')):
	if os.path.isdir(os.path.join(opt.crop_dir,'fake_real',directory)):
		if not os.path.exists(os.path.join(opt.tmp_dir,'fake_real',directory)):
			if len(os.listdir(os.path.join(opt.crop_dir,'fake_real',directory)))==0:
				continue
			videoName = os.listdir(os.path.join(opt.crop_dir,'fake_real',directory))[0]
			videopath = os.path.join(opt.crop_dir,'fake_real',directory,videoName)
			framedir = os.path.join(opt.crop_dir,'fake_real',directory,'frames')
			os.makedirs(framedir)

			audiodir = os.path.join(opt.crop_dir,'fake_real',directory)

			command = ("ffmpeg -y -i %s -qscale:v 2 -threads 1 -f image2 %s" % (videopath,os.path.join(framedir,'%06d.jpg')))
			output = subprocess.call(command, shell=True, stdout=None)

			command = ("ffmpeg -y -i %s -ac 1 -vn -acodec pcm_s16le -ar 48000 %s" % (videopath, os.path.join(audiodir,'audio.wav')))
			output = subprocess.call(command, shell=True, stdout=None)

for video in tqdm.tqdm(os.listdir(opt.real_dir)):
	if not os.path.exists(os.path.join(opt.data_dir,'pycrop','real_real',os.path.basename(video)[0:-4])):
		print(video)
		run_pipeline(opt.data_dir,os.path.join(opt.real_dir,video),os.path.basename(video)[0:-4],'real_real')

for directory in os.listdir(os.path.join(opt.crop_dir,'real_real')):
	if os.path.isdir(os.path.join(opt.crop_dir,'real_real',directory)):
		if not os.path.exists(os.path.join(opt.tmp_dir,'real_real',directory)):
			if len(os.listdir(os.path.join(opt.crop_dir,'real_real',directory)))==0:
				continue
			videoName = os.listdir(os.path.join(opt.crop_dir,'real_real',directory))[0]
			videopath = os.path.join(opt.crop_dir,'real_real',directory,videoName)
			framedir = os.path.join(opt.crop_dir,'real_real',directory,'frames')
			os.makedirs(framedir)

			audiodir = os.path.join(opt.crop_dir,'real_real',directory)

			command = ("ffmpeg -y -i %s -qscale:v 2 -threads 1 -f image2 %s" % (videopath,os.path.join(framedir,'%06d.jpg')))
			output = subprocess.call(command, shell=True, stdout=None)

			command = ("ffmpeg -y -i %s -ac 1 -vn -acodec pcm_s16le -ar 48000 %s" % (videopath, os.path.join(audiodir,'audio.wav')))
			output = subprocess.call(command, shell=True, stdout=None)

