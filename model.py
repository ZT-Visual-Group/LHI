import torch
import config
import torch.nn as nn
from torchvision import models
import torch.nn.functional as F
from utils import *
from backbone.resnet import *
from backbone.HIL import *
import operator
from config import args_setting

def generate_model(args):

    use_cuda = args.cuda and torch.cuda.is_available()
    device = torch.device("cuda" if use_cuda else "cpu")

    assert args.model in [ 'CMDF', 'CNN_3D', 'CNN_2D', 'AUDIO', "IMAGE"]
    if args.model == 'CMDF':
        model = CMDF().to(device)
    elif args.model == 'CNN_3D':
        model = CNN_3D().to(device)
    elif args.model == 'CNN_2D':
        model =CNN_2D(config.img_channel, config.class_num).to(device)
    elif args.model == 'IMAGE':
        model =IMAGE(config.img_channel, config.class_num).to(device)
    elif args.model == 'AUDIO':
        model = AUDIO(config.img_channel, config.class_num).to(device)
    return model

class CNN_2D(nn.Module):
    def __init__(self, n_channels, n_classes):
        super(CNN_2D, self).__init__()
        self.AHIL = AHILBlock(512, 256)
        model = models.resnet18(pretrained=True)
        self.model = nn.Sequential(*list(model.children())[:-2])
        self.final_pool = nn.AdaptiveAvgPool2d(1)
        self.lstm = nn.LSTM(512, 512, 1, False)
        self.fin_fc = nn.Sequential(nn.Linear(512, 2))

    def forward(self, x):
        x = torch.unbind(x, dim=1)
        data = []
        for item in x:
            x6 = self.model(item)
            data.append(x6.unsqueeze(0))
        data = torch.cat(data, dim=0)
        seq_length, batch_size, c, h, w = data.size()
        x = data.view(batch_size * seq_length, c, h, w)
        x = self.final_pool(x)
        x = x.view(seq_length, batch_size, c).transpose(1, 0)
        x, _ = self.lstm(x, None)
        x = self.fin_fc(torch.mean(x, dim=1))
        return x


class CNN_3D(nn.Module):
    def __init__(self):
        super(CNN_3D,self).__init__()
        self.videonet = resnet34(num_classes=2, sample_size=224, sample_duration=30)
        self.videonet.load_state_dict({k.split('.', 1)[1]: v for k, v in torch.load(
            './model_weights/resnet-34-kinetics.pth')['state_dict'].items() if 'fc.' not in k},strict=False)

    def forward(self, x):
        print("CNN_3D")
        for name, module in self.videonet.named_children():
            x = module(x)
            if name == "avgpool":
                x = x.view(x.shape[0], -1)
        return x


class CMDF(nn.Module):
    def __init__(self):
        super(CMDF,self).__init__()
        self.videonet = resnet34(num_classes=2,sample_size=224, sample_duration=30)
        #self.videonet.load_state_dict({k.split('.',1)[1]:v for k,v in torch.load('model_weights/resnet-34-kinetics.pth')['state_dict'].items() if 'fc.' not in k},
        #strict=False)
        self.audionet = models.resnet34(pretrained=True).cuda()
        self.num_ftrs = self.audionet.fc.in_features
        self.audionet.fc = nn.Linear(self.num_ftrs, 256)
        self.keyframenet = CNN_2D(config.img_channel, config.class_num).cuda()
        self.EHIL = EHILBlock(in_channels=768, out_channels=512)
        self.MHIL = MHILBlock(512, 512)
        self.avgpool_2d = nn.AdaptiveAvgPool2d(1)
        self.final_fc = nn.Sequential(nn.Linear(1280, 2))
        self.audio_feature = 0


    def forward(self, x, x1, x2):
        data = []
        for name, module in self.keyframenet.named_children():
            if name == "model":
                x1 = torch.unbind(x1, dim=1)
                for item in x1:
                    x1 = module(item)
                    data.append(x1.unsqueeze(0))
                data = torch.cat(data, dim=0)
                data1 = data.transpose(1, 0)
                data1 = data1.transpose(2, 1)
                feature_2d = F.avg_pool3d(data1, (5, 1, 1), stride=(1, 1, 1))
                feature_2d = feature_2d.squeeze(2)
                feature_2d = self.keyframenet.AHIL(feature_2d)
            elif name == "final_pool":
                seq_length, batch_size, c, h, w = data.size()
                x1 = data.view(batch_size * seq_length, c, h, w)
                x1 = module(x1)
                x1 = x1.view(seq_length, batch_size, c)
                x1 = x1.transpose(1, 0)
            elif name == "lstm":
                x1, _ = module(x1, None)
                lstm_output = torch.mean(x1, dim=1)
            elif name == "fin_fc":
                x1 = module(torch.mean(x1, dim=1))

        for name, module in self.videonet.named_children():
            x = module(x)
            if name == "avgpool":
                x = x.view(x.shape[0], -1)
            if name == "layer4":
                feature = F.avg_pool3d(x, (2, 1, 1), stride=(1, 1, 1))
                feature = feature.squeeze(2)


        for name, module in self.audionet.named_children():
            if name == "avgpool":
                x2 = self.MHIL(x2)
            x2 = module(x2)
            if name == "avgpool":
                x2 = x2.view(x2.size()[0], -1)
            if name == "fc":
                self.audio_feature = x2
        x3 = torch.cat((feature, feature_2d), dim=1)
        x3 = self.EHIL(x3)
        x3 = self.avgpool_2d(x3)
        x3 = x3.view(x3.size()[0], -1)
        x3 = torch.cat((x3, lstm_output), dim=1)
        x3 = torch.cat((x3, self.audio_feature), dim=1)
        final_feature = x3
        x3 = self.final_fc(x3)

        return x3, final_feature


class IMAGE(nn.Module):
    def __init__(self, n_channels, n_classes):
        super(IMAGE, self).__init__()
        self.model = models.resnet18(pretrained=True)
        num_ftrs = self.model.fc.in_features
        self.model.fc = nn.Linear(num_ftrs, n_classes)

    def forward(self, x):
        feature_fc =  np.zeros((x.shape[0], 512))
        for name, module in self.model.named_children():
            x = module(x)
            if name == "avgpool":
                x = x.view(x.shape[0], -1)
                feature_fc = x
        return x, feature_fc


class AUDIO(nn.Module):
    def __init__(self, n_channels, n_classes):
        super(AUDIO, self).__init__()
        self.model = models.resnet18(pretrained=True)
        num_frts = self.model.fc.in_features
        self.model.fc = nn.Linear(num_frts, n_classes)

    def forward(self, x):
        x = self.model(x)
        return x
