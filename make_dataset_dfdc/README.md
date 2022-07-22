## DFDC Dataset Build Pipline
  
1、Create the floder under "DFDC" named "dfdc_work_dir". The folder structure is as follows:  
```
DFDC
├── dfdc_work_dir
```  
  
2、The original fake samples can be download here [DFDC_Original](https://www.kaggle.com/c/deepfake-detection-challenge/data). And unzip smaples into "DFDC/". Then the folder structure is changed as the following:
```DFDC
├── dfdc_work_dir
├── dfdc_train_part_0
├── dfdc_train_part_1
├── dfdc_train_part_2
├── dfdc_train_part_3
├── dfdc_train_part_4
├── ...
``` 
  
Noting that there are 50 dfdc_train_part_* floders under the directory of "DFDC/".
  
3、Congratulations, you can get our DFDC dataset by running the scripts 1-6 in sequence. 
  
```
0_0_move_dfdc_videos.py
0_find_fake_audio.py
1_find_all_real_fake_group.py
2_audio_video_split.py
3_merge_correspinding_data.py
4_move_video_final_dir.py
5_pre-process.py
6_data_clean.py

``` 

