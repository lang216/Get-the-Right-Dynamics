import numpy as np
import librosa

def analyze_audio(audio_file):
    # Load audio file and calculate the Short-time Fourier Transform (STFT)
    y, sample_rate = librosa.load(audio_file, mono=True)
    stft_result = librosa.stft(y, n_fft=2048)

    # Calculate the corresponding frequencies
    frequencies = librosa.core.fft_frequencies(sr=sample_rate, n_fft=stft_result.shape[0])

    # Convert the amplitude to dB
    stft_result_db = librosa.amplitude_to_db(np.abs(stft_result), ref=np.max)
    #weighted_stft_db = librosa.perceptual_weighting(abs(y)**2, frequencies)

    return frequencies, stft_result_db, sample_rate#, weighted_stft_db

def find_amplitudes_in_db(timepoints, frequency_lists, frequencies, stft_result_db, duration, sample_rate):
    """
    Calculate the amplitudes in dB at specific timepoints and frequencies using linear interpolation.

    Parameters:
        timepoints (list): List of timepoints in seconds.
        frequency_lists (list): List of lists containing frequencies in Hz.
        frequencies (numpy.ndarray): Array of frequencies corresponding to STFT result.
        stft_result_db (numpy.ndarray): STFT result of the audio signal in dB.
        duration (float): Duration of the audio in seconds.
        sample_rate (int): Sample rate of the audio.

    Returns:
        list: A 2D list containing the amplitudes (in dB) for each combination of timepoint and frequency.
    """
    amplitudes_db = []
    
    for timepoint, freq_list in zip(timepoints, frequency_lists):
        if timepoint < 0 or timepoint > duration:
            raise ValueError(f"Timepoint {timepoint} seconds is out of range.")
        
        index = int(timepoint / duration * stft_result_db.shape[1])
        time_amplitudes_db = []
        
        for frequency in freq_list:
            if frequency < frequencies[0] or frequency > frequencies[-1]:
                # Frequency is out of range, find the nearest frequency in the array
                closest_freq_index = np.argmin(np.abs(frequencies - frequency))
                x1, x2 = frequencies[closest_freq_index - 1], frequencies[closest_freq_index]
                y1, y2 = stft_result_db[closest_freq_index - 1, index], stft_result_db[closest_freq_index, index]
                slope = (y2 - y1) / (x2 - x1)
                time_amplitudes_db.append(y1 + slope * (frequency - x1))
            else:
                frequency_index = np.searchsorted(frequencies, frequency)
                if frequency_index == 0:
                    time_amplitudes_db.append(stft_result_db[frequency_index, index])
                else:
                    x1, x2 = frequencies[frequency_index - 1], frequencies[frequency_index]
                    y1, y2 = stft_result_db[frequency_index - 1, index], stft_result_db[frequency_index, index]
                    slope = (y2 - y1) / (x2 - x1)
                    time_amplitudes_db.append(y1 + slope * (frequency - x1))
        
        amplitudes_db.append(time_amplitudes_db)
    
    return amplitudes_db