from flask import Flask, render_template, request, redirect
import speech_recognition as spr
import torch
import librosa
import numpy as np
import random
import os
import pandas as pd
import os
import datetime
import scipy
import glob
import math
import warnings
import pickle
import soundfile as sf
from sklearn.utils import shuffle
import sources.utils as utils
from sources.FeatureExtractor import FeatureExtractor
# import config from sources.utils
import sources.models as sm



app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    path = ""
    file_name = ""
    transcript = ""
    path1 = ""

    if request.method == "POST":
        print("FORM DATA RECEIVED")

        if "file" not in request.files:
            return redirect(request.url)

        file = request.files["file"]
        if file.filename == "":
            return redirect(request.url)

        if file:
            file_name = str(random.randint(0, 100000))+'.wav'
            path = "static/audio/noisy"
            file.save(os.path.join(path, file_name))
            audio, sr = librosa.load(path + '/' + file_name)

            recognizer = spr.Recognizer()
            audioFile = spr.AudioFile(file)
            transcript = str(audio.shape)
            path =  "../static/audio/noisy/" + file_name
            noisyAudio, sr = utils.read_audio(path[3:], sample_rate=utils.config['fs'])
            # sf.write(path[3:]+file_name,noisyAudio,sr)
            noiseAudioFeatureExtractor = FeatureExtractor(noisyAudio, 
                                                          windowLength=utils.config['windowLength'], 
                                                          overlap=utils.config['overlap'], 
                                                          sample_rate=utils.config['fs'])
            noise_stft_features = noiseAudioFeatureExtractor.get_stft_spectrogram()
            noisyPhase = np.angle(noise_stft_features)
            noise_stft_features = np.abs(noise_stft_features)
            predictors = utils.prepare_input_features_inference(noise_stft_features)
            predictors = np.reshape(predictors, (predictors.shape[0], predictors.shape[1], 1, predictors.shape[2]))
            predictors = np.transpose(predictors, (3, 2, 0, 1)).astype(np.float32)
            predictors = (torch.from_numpy(predictors))

            model = sm.MyModel22()
            model_path = 'sources/model_weight/model22_1.pth'
            model.load_state_dict(torch.load(model_path,map_location=torch.device('cpu'))) 

            STFTFullyConvolutional = model(predictors)
            denoisedAudioFullyConvolutional = utils.revert_features_to_audio(STFTFullyConvolutional.detach().numpy(), 
                                                                             noisyPhase, noiseAudioFeatureExtractor)
            path1 = "../static/audio/denoised/" + file_name
            sf.write(path1[3:],denoisedAudioFullyConvolutional,sr)

            # print(denoisedAudioFullyConvolutional.shape)  


    return render_template('index.html', transcript=transcript, path = path , path1 = path1)


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
