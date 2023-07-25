import numpy as np
import librosa
from audio_processing import *
from utilities import *

# Replace 'your_audio_file.wav' with the path to your audio file
audio_file = 'Get the Right Dynamics/input_audio.wav'
frequencies, stft_result, sample_rate = analyze_audio(audio_file)
duration = librosa.get_duration(filename=audio_file)

# timepoints = [0.1,0.2,0.3,0.4]
# list_of_frequencies = [[5000,600],[1334],[4561],[100, 900, 1000]]

timepoints_OM = read_txt_file('input_timepoints.txt') # seconds, should be a list of timepoints
timepoints = om_to_python(timepoints_OM)
list_of_frequencies_OM = read_txt_file('input_frequencies.txt') # Hz, should be a list of frequencies
list_of_frequencies = om_to_python(list_of_frequencies_OM)

loudness = find_amplitudes(timepoints, frequency_lists=list_of_frequencies, frequencies=frequencies, stft_result=stft_result, duration=duration, sample_rate=sample_rate)
loudness_OM = convert_to_om(loudness)

with open('Get the Right Dynamics/output.txt', 'w') as f:
    f.write('Loudness Measured in DB: '+str(loudness_OM))

