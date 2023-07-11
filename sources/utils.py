import librosa
import pandas as pd
import os
import datetime
import numpy as np
import scipy
import glob
import numpy as np
import math
import warnings
import pickle
from sklearn.utils import shuffle

windowLength = 256
ffTLength    = windowLength 
numFeatures  = ffTLength//2 + 1
numSegments  = 16

config = dict(
    windowLength = windowLength,
    overlap      = round(0.25 * windowLength), 
    ffTLength    = windowLength,
    fs           = 16000,
    numFeatures  = ffTLength//2 + 1,
    numSegments  = 16

    )

def read_audio(filepath, sample_rate, normalize=False):
    audio, sr = librosa.load(filepath, sr=sample_rate)
    if normalize:
        div_fac = 1 / np.max(np.abs(audio)) / 3.0
        audio = audio * div_fac
    return audio, sr
        

def add_noise_to_clean_audio(clean_audio, noise_signal):
    if len(clean_audio) >= len(noise_signal):
        while len(clean_audio) >= len(noise_signal):
            noise_signal = np.append(noise_signal, noise_signal)

    ind = np.random.randint(0, noise_signal.size - clean_audio.size)

    noiseSegment = noise_signal[ind: ind + clean_audio.size]

    speech_power = np.sum(clean_audio ** 2)
    noise_power = np.sum(noiseSegment ** 2)
    noisyAudio = clean_audio + np.sqrt(speech_power / noise_power) * noiseSegment
    return noisyAudio


def prepare_input_features_inference(stft_features,name):

    if name == "MyModel":
        numSegments = 8
    else: numSegments = 16
    
    noisySTFT = np.concatenate([stft_features[:,0:numSegments-1], stft_features], axis=1)
    stftSegments = np.zeros((numFeatures, numSegments , noisySTFT.shape[1] - numSegments + 1))

    for index in range(noisySTFT.shape[1] - numSegments + 1):
        stftSegments[:,:,index] = noisySTFT[:,index:index + numSegments]
    return stftSegments


def revert_features_to_audio(features, phase, FeatureExtractor, cleanMean=None, cleanStd=None):
    if cleanMean and cleanStd:
        features = cleanStd * features + cleanMean
    phase = np.transpose(phase, (1, 0))
    features = np.squeeze(features)

    features = features * np.exp(1j * phase)  

    features = np.transpose(features, (1, 0))
    return FeatureExtractor.get_audio_from_stft_spectrogram(features)