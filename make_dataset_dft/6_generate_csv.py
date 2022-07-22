import os
import shutil
from make_dataset_dft import dataset_config


a = open("label_2.csv","w")
path = dataset_config.crop_face_save_path

for i in range(len(os.listdir(os.path.join(path, "fake_fake")))-7):
    a.write(os.listdir(os.path.join(path, "fake_real"))[i]+" fake"+" real"+" fake\n")
    a.write(os.listdir(os.path.join(path, "real_fake"))[i] + " real" + " fake" + " fake\n")
    a.write(os.listdir(os.path.join(path, "fake_fake"))[i]+" fake"+" fake"+" fake\n")
    a.write(os.listdir(os.path.join(path, "real_real"))[i]+" real"+" real"+" real\n")

a.close()

train_file = open("label_train.csv", "w")
test_file = open("label_test.csv", "w")
with open("label_2.csv", "r") as b:
    lines = b.readlines()
    print(len(lines))
    for line in lines[:-186]:
        train_file.write(line)
    for line in lines[-186:]:
        test_file.write(line)
