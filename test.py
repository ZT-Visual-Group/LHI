import torch
import config
from config import args_setting
from dataset import RoadSequenceDataset, RoadSequenceDatasetList, RoadAudioDataset
from model import generate_model
from torchvision import transforms
from torch.optim import lr_scheduler
from PIL import Image
import numpy as np
import cv2
from sklearn.metrics import roc_curve
from sklearn.metrics import auc
import matplotlib.pyplot as plt

def evaluate_model(model, test_loader, device, criterion):
    i = 0
    test_loss = 0
    correct = 0
    with torch.no_grad():
        for batch_idx, sample_batched in enumerate(test_loader):
            i+=1
            if args.model == "CMDF":
                data, data_2d, data_aud, target = sample_batched['data'].to(device), sample_batched['data_2d'].to(device), sample_batched['data_aud'].to(device), sample_batched['label'].type(torch.LongTensor).to(device)
            else:
                data, data_2d, target = sample_batched['data'].to(device), sample_batched['data_2d'].to(
                    device), sample_batched['label'].type(torch.LongTensor).to(
                    device)

            if args.model == "CMDF":
                output, final_feature = model(data, data_2d, data_aud)
            elif args.model == "CNN_2D":
                output = model(data_2d)
            else:
                output = model(data)
            #accuracy
            loss = criterion(output, target).item()
            test_loss += criterion(output, target).item()  # sum up batch loss
            pred = output.max(1, keepdim=True)[1]
            correct += pred.eq(target.view_as(pred)).sum().item()
            if batch_idx % 5 == 0:
                print('Test [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
                    batch_idx * len(data), len(test_loader.dataset),
                    100. * batch_idx / len(test_loader), loss))
    test_loss /= (len(test_loader.dataset) / args.test_batch_size)
    test_acc = 100. * int(correct) / len(test_loader.dataset)
    print('\nAverage loss: {:.4f}, Accuracy: {}/{} ({:.5f}%)'.format(
        test_loss, int(correct), len(test_loader.dataset), test_acc))


if __name__ == '__main__':
    args = args_setting()
    torch.manual_seed(args.seed)
    use_cuda = args.cuda and torch.cuda.is_available()
    device = torch.device("cuda" if use_cuda else "cpu")

    #turn image into floatTensor
    op_tranforms = transforms.Compose([transforms.ToTensor()])
    op_tranforms_2d = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    # load data for batches, num_workers for multiprocess
    if args.model == "IMAGE":
        test_loader = torch.utils.data.DataLoader(
            RoadSequenceDataset(file_path=config.test_path, transforms=op_tranforms_2d),
            batch_size=6, shuffle=False, num_workers=config.data_loader_numworkers)
    elif args.model == "AUDIO":
        test_loader = torch.utils.data.DataLoader(
            RoadAudioDataset(file_path=config.val_path, transforms=op_tranforms),
            batch_size=1, shuffle=False, num_workers=config.data_loader_numworkers)
    else:
        test_loader = torch.utils.data.DataLoader(
            RoadSequenceDatasetList(file_path=config.test_path, transforms=op_tranforms, transforms_2d=op_tranforms_2d),
            batch_size=6, shuffle=False, num_workers=config.data_loader_numworkers)


    # load model and weights
    model = generate_model(args)
    criterion = torch.nn.CrossEntropyLoss().to(device)

    pretrained_dict = torch.load(config.pretrained_path)
    model_dict = model.state_dict()
    pretrained_dict_1 = {k: v for k, v in pretrained_dict.items() if (k in model_dict)}
    model_dict.update(pretrained_dict_1)
    model.load_state_dict(model_dict)

    # calculate the values of accuracy
    evaluate_model(model, test_loader, device, criterion)
