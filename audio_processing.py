import numpy as np
import librosa

def analyze_audio(audio_file):
    # Load audio file and calculate the Short-time Fourier Transform (STFT)
    y, sample_rate = librosa.load(audio_file, mono=True)
    stft_result = librosa.stft(y)

    # Calculate the corresponding frequencies
    frequencies = librosa.fft_frequencies(sr=sample_rate, n_fft=stft_result.shape[0])

    return frequencies, stft_result, sample_rate


def find_amplitudes(timepoints, frequency_lists, frequencies, stft_result, duration, sample_rate):
    """
    Calculate the amplitudes at specific timepoints and frequencies using linear interpolation.

    Parameters:
        timepoints (list): List of timepoints in seconds.
        frequency_lists (list): List of lists containing frequencies in Hz.
        frequencies (numpy.ndarray): Array of frequencies corresponding to STFT result.
        stft_result (numpy.ndarray): STFT result of the audio signal. (converted to DB)
        duration (float): Duration of the audio in seconds.
        sample_rate (int): Sample rate of the audio.

    Returns:
        list: A 2D list containing the amplitudes for each combination of timepoint and frequency.
    """
    amplitudes = []
    stft_result = librosa.amplitude_to_db(abs(stft_result))
    
    for timepoint, freq_list in zip(timepoints, frequency_lists):
        if timepoint < 0 or timepoint > duration:
            raise ValueError(f"Timepoint {timepoint} seconds is out of range.")
        
        index = int(timepoint / duration * stft_result.shape[1])
        time_amplitudes = []
        
        for frequency in freq_list:
            if frequency < frequencies[0] or frequency > frequencies[-1]:
                time_amplitudes.append(None)  # Frequency is out of range
            else:
                frequency_index = np.searchsorted(frequencies, frequency)
                if frequency_index == 0:
                    time_amplitudes.append(np.abs(stft_result[frequency_index, index]))
                else:
                    x1, x2 = frequencies[frequency_index - 1], frequencies[frequency_index]
                    y1, y2 = np.abs(stft_result[frequency_index - 1, index]), np.abs(stft_result[frequency_index, index])
                    slope = (y2 - y1) / (x2 - x1)
                    time_amplitudes.append(y1 + slope * (frequency - x1))
        
        amplitudes.append(time_amplitudes)
    
    return amplitudes