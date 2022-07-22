import argparse

# globel param
# dataset setting
img_width = 224
img_height = 224
img_channel = 3
data_loader_numworkers = 8
class_num = 2

code_work_path = "path to LHI"
multi_modal_dataset_save_path = "path to /DeepFake-TIMIT/our-timit-2/pycrop/"
# path
train_path = code_work_path + "make_dataset_dft/label_train.csv"
val_path = code_work_path + "make_dataset_dft/label_test.csv"
test_path = code_work_path +  "make_dataset_dft/label_test.csv"
save_path = code_work_path + "save"
pretrained_path=code_work_path + 'save/100.0_HQ.pth'

# weight
class_weight = [0.25, 0.75]

# CMDF batch_size:6, test_batch_size:12,
# CNN_2D batch_size:6
def args_setting():
    # Training settings
    parser = argparse.ArgumentParser(description='PyTorch CMDF')
    parser.add_argument('--model',type=str, default='CMDF',help='( CMDF | CNN_3D | CNN_2D | AUDIO | IMAGE')
    parser.add_argument('--batch-size', type=int, default=6, metavar='N',
                        help='input batch size for training (default: 10)')
    parser.add_argument('--test-batch-size', type=int, default=12, metavar='N',
                        help='input batch size for testing (default: 100)')
    parser.add_argument('--epochs', type=int, default=70, metavar='N',
                        help='number of epochs to train (default: 50)')
    parser.add_argument('--lr', type=float, default=0.001, metavar='LR',
                        help='learning rate (default: 0.01)')
    parser.add_argument('--momentum', type=float, default=0.9, metavar='M',
                        help='SGD momentum (default: 0.9)')
    parser.add_argument('--cuda', action='store_true', default=True,
                        help='use CUDA training')
    parser.add_argument('--seed', type=int, default=1, metavar='S',
                        help='random seed (default: 1)')
    parser.add_argument('--log-interval', type=int, default=10, metavar='N',
                        help='how many batches to wait before logging training status')
    args = parser.parse_args()
    return args
