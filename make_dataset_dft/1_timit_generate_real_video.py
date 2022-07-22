import os
import shutil
import subprocess
import cv2
from make_dataset_dft import dataset_config

fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')
fps = 30
timit_real_path = dataset_config.timit_real_path
timit_real_save_path = dataset_config.timit_real_save_path

def generate_real_Video(vidname):
    global path, timit_real_save_path
    for audname in os.listdir(os.path.join(timit_real_path, vidname, "video")):
        if "head" not in audname:
            real_video_name = timit_real_save_path+"/0_"+vidname+"_"+audname+".avi"
            real_audio_name = os.path.join(timit_real_path, vidname, "audio", audname+".wav")
            real_real_save_path = timit_real_save_path+"/00_"+vidname+"_"+audname+".avi"
            print("/0_"+vidname+"_"+audname+".avi", vidname+"/audio/"+ audname+".wav", )
            videoWrite = cv2.VideoWriter(real_video_name, fourcc, fps, (512, 384))
            img_names = []

            for i in os.listdir(os.path.join(timit_real_path, vidname, "video", audname)):
                img_names.append(i)
            img_names.sort()
            for j in img_names:
                img = cv2.imread(os.path.join(timit_real_path, vidname, "video", audname, j))
                videoWrite.write(img)
            videoWrite.release()
            command = ("ffmpeg -i %s -i %s -c:v copy -c:a aac -strict experimental %s"%(real_video_name, real_audio_name, real_real_save_path))
            output = subprocess.call(command, shell=True, stdout=None)
            os.remove(real_video_name)

if __name__ == '__main__':
    if not os.path.exists(timit_real_save_path):
        os.makedirs(timit_real_save_path)
    for video_name in os.listdir(timit_real_path):
        generate_real_Video(video_name)



