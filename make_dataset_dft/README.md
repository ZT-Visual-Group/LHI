## DeepFake-TIMIT-LQ Dataset Build Pipline
  
1、Create the floder under "DeepFake-TIMIT" named "DeepFake-TIMIT" and "DeepFake-TIMIT-REAL". The folder structure is as follows:  
```
DeepFake-TIMIT
├── DeepFake-TIMIT
├── DeepFake-TIMIT-REAL
```  
  
2、The original fake samples can be download here [Fake](https://www.idiap.ch/en/dataset/deepfaketimit) and [Real](https://conradsanderson.id.au/vidtimit/). And put "Fake" smaples into "DeepFake-TIMIT/DeepfakeTIMIT", and unzip "Real" samples in "DeepFake-TIMIT/DeepFake-TIMIT-REAL". Then the folder structure is changed as the following:
```
DeepFake-TIMIT
├── DeepfakeTIMIT
├────── higher_quality
├────── lower_quality
├── DeepFake-TIMIT-REAL
├────── fadg0
├────── faks0
├────── ...
``` 
  
Noting that there are 32 floders under the directory of "DeepFake-TIMIT-REAL/", including fadg0, faks0, fcft0, fcmh0, fdac1, fdrd1, fedw0, felc0, fjas0, fjem0, fjre0, fjwb0, fkms0, fram1, mccs0, mcem0, mdab0, mdbb0, mdld0, mgwt0, mjar0, mjsw0, mmdb1, mmdm2, mpdf0, mpgl0, mrcz0, mrgg0, mrjo0, msjs1, mstk0, mwbt0. And it is important to delete the rest subfloders!!!   
  
3、Congratulations, you can get our DeepFake-TIMIT dataset by running the scripts 1-6 in sequence. 
  
```
1_timit__generate_real_video.py
2_timit__generate_fake_video.py
3_extract_normal_face.py
4_generate_fake_audio.py
5_data_clean.py
6_generate_csv.py

``` 

## DeepFake-TIMIT-HQ Dataset Build Pipline
1、Just change "timit_fake_path" in "LHI/make_dataset_dft/dataset_config.py" to ```/DeepfakeTIMIT/higher_quality``` , and change "our-timit-2" to "our-timit-3" in the line 4 and 10 of "MMFD-ACMMM/make_dataset_dft/dataset_config.py".


