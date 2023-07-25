import numpy as np
import librosa
from audio_processing import *
from utilities import *

# Replace 'your_audio_file.wav' with the path to your audio file
audio_file = "C:/Users/langc/OneDrive/Lang Chen/Compositions/2023/full orchestra/mixed_texture-out(strectched).wav"
frequencies, stft_result_db, sample_rate = analyze_audio(audio_file)
duration = librosa.get_duration(path=audio_file)

timepoints_OM = read_txt_file('Get-the-Right-Dynamics-main/input_timepoints.txt') # seconds, should be a list of timepoints
timepoints = [timp/1000 for timp in om_to_python(timepoints_OM)[0]]
list_of_frequencies_OM = read_txt_file('Get-the-Right-Dynamics-main/input_frequencies.txt') # Hz, should be a list of frequencies
list_of_frequencies = om_to_python(list_of_frequencies_OM)
B_weighted_freqs = librosa.B_weighting(list_of_frequencies)

loudness = find_amplitudes_in_db(timepoints, list_of_frequencies, frequencies, stft_result_db, duration, sample_rate)
weighted_loudness = loudness + B_weighted_freqs
weighted_loudness = [float(w_l) for w_l in weighted_loudness]
loudness_OM = convert_to_om(weighted_loudness)

midi_velocities = db_to_midi_velocity(list(weighted_loudness), max(list(weighted_loudness)), min(list(weighted_loudness)))
midi_velocities_OM = convert_to_om(midi_velocities)

music_dynamics = midi_velocity_to_dynamic(midi_velocities)
music_dynamics_OM = convert_to_om(music_dynamics)

with open('Get-the-Right-Dynamics-main/output.txt', 'w') as f:
    f.write('Loudness Measured in DB (B-Weighting): '+str(loudness_OM)+'\n'+'\n')
    f.write('MIDI Velocity Values: '+str(midi_velocities_OM)+'\n'+'\n')
    f.write('Music Dynamics: '+str(music_dynamics_OM))

