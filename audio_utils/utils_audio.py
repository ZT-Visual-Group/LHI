import librosa
import numpy as np
import random

def mono_to_color(X, eps=1e-6, mean=None, std=None):
    """
    Converts a one channel array to a 3 channel one in [0, 255]
    Arguments:
        X {numpy array [H x W]} -- 2D array to convert
    Keyword Arguments:
        eps {float} -- To avoid dividing by 0 (default: {1e-6})
        mean {None or np array} -- Mean for normalization (default: {None})
        std {None or np array} -- Std for normalization (default: {None})
    Returns:
        numpy array [3 x H x W] -- RGB numpy array
    """
    X = np.stack([X, X, X], axis=0)


    mean = mean or X.mean()
    std = std or X.std()
    X = (X - mean) / (std + eps)


    _min, _max = X.min(), X.max()

    if (_max - _min) > eps:
        V = np.clip(X, _min, _max)
        V = 255 * (V - _min) / (_max - _min)
        V = (V - _min) / (_max - _min)
        V = V.astype(np.uint8)
    else:
        V = np.zeros_like(X, dtype=np.uint8)

    return V


def normalize(image, mean=None, std=None):
    """
    Normalizes an array in [0, 255] to the format adapted to neural network
    Arguments:
        image {np array [3 x H x W]} -- [description]
    Keyword Arguments:
        mean {None or np array} -- Mean for normalization, expected of size 3 (default: {None})
        std {None or np array} -- Std for normalization, expected of size 3 (default: {None})
    Returns:
        np array [H x W x 3] -- Normalized array
    """
    image = image / 255.0
    if mean is not None and std is not None:
        image = (image - mean) / std
    return np.array(image).astype(np.float32)


def pad_clip(y, sr, size):
    len_y = y.shape[0] / sr
    width = "long"
    if(len_y<=size):
        zeroo = np.zeros(size*sr-y.shape[0])
        y = np.concatenate((y,zeroo))
        width = "short"
    else:
        start = random.randint(0, len(y) - size * sr)
        y = y[start: start + size * sr]
    return y, width

def extract_logmel(y, sr, size, spec_height, spec_width, fmin, fmax):
    y, width = pad_clip(y, sr, size)

    NUM_MELS = spec_height
    HOP_LENGTH = int(32000 * 5 / (spec_width - 1))  # sample rate * duration / spec width
    mel_spec = librosa.feature.melspectrogram(y,
                                              sr=sr,
                                              n_fft=1024,
                                              hop_length=HOP_LENGTH,
                                              n_mels=NUM_MELS,
                                              fmin=fmin,
                                              fmax=fmax)

    mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)

    mel_spec_db = mono_to_color(mel_spec_db)
    mel_spec_db = normalize(mel_spec_db)

    # el_spec_db = np.stack([mel_spec_db, mel_spec_db, mel_spec_db], axis=0)
    # el_spec_db -= mel_spec_db.min()
    # el_spec_db /= mel_spec_db.max()

    return mel_spec_db, width