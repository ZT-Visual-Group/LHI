# LHI

## Description
The code, dataset and models of the paper(Learning Heterogeneous Inconsistency for Multimodal Face Forgery Detection). 

## Installation
1、ffmpeg  
  
2、pytorch 1.7.0 & torchvision & torchsummary  
  
The rest dependencies can be installed by running the command  
```pip install -r requirements.txt```  

## Our Datasets
  
### DeepFake-TIMIT Dataset  
1、Create a folder named "DeepFake-TIMIT" as your work_dir, and then modify the path of "work_dir" in "LHI/make_dataset_dft/dataset_config.py" to your own path.
  
2、Download publicly available face detection weights from [S3FD](https://drive.google.com/file/d/1miORz3wom1DfXF0iktVV1VG0P_lK79Lh/view?usp=sharing), and put it into "make_dataset_dft/detectors/s3fd/weights/".  
  
3、The following steps can be seen in the "make_dataset_dft/README.md".  
  
### DFDC Dataset
1、Create a folder named "DFDC" as your work_dir, and then modify the path of "dfdc_save_path" in "LHI/make_dataset_dfdc/dfdc_dataset_config.py" to your own path.
  
2、Download publicly available face detection weights from [S3FD](https://drive.google.com/file/d/1miORz3wom1DfXF0iktVV1VG0P_lK79Lh/view?usp=sharing), and put it into "make_dataset_dfdc/detectors/s3fd/weights/".  
  
3、The following steps can be seen in the "make_dataset_dfdc/README.md".  
  
## Model Reproduction
1、After geting our dataset, you can download our trained models from [DFT-HQ](https://drive.google.com/file/d/14Hdj-Kyun7u3sIwTLov1vnKU09i6D_HP/view?usp=sharing), [DFT-LQ](https://drive.google.com/file/d/1XxZCzAr0LqCZCQXHkp84gU1SK6HQLF1V/view?usp=sharing) and [DFDC](https://drive.google.com/file/d/1RpWpl23JRRuV1elJu5l-PF4eM2cDXu-g/view?usp=sharing). And put them into directory "LHI/save/", change the pretrained model path in "LHI/config.py(pretrained_path(line 16))".
   
2、There are other two path in "config.py" should be changed to your own path:
```
a) code_work_path # the path to LHI
b) multi_modal_dataset_save_path # the path to DeepFake-TIMIT
```  
  
3、run "test.py". 

## Train
The train code will be released here after the paper published.

