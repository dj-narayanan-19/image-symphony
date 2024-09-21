import cv2
import numpy as np
from pydub import AudioSegment
from extractHorizon import *


def generate_frequencies(start_freq, octaves):
    """
    Generate an array of frequencies for a given starting frequency and number of octaves.

    Parameters:
    - start_freq: The starting frequency (e.g., for A4 it's 440 Hz).
    - octaves: The number of octaves to generate frequencies for.

    Returns:
    - A numpy array of frequencies for all the notes in the specified range.
    """
    frequencies = []
    for i in range(int(octaves * 12)):  # Ensure octaves * 12 is an integer
        freq = start_freq * (2 ** (i / 12))
        frequencies.append(freq)
    return np.array(frequencies)

# takes frequency value and converts it to a common musical scale
def instrument_frequency(array1, instrument_array):
    frequency_raw = map_horizon(array1, min(array1), max(array1), min(instrument_array), max(instrument_array))
    # Reshape frequencies to be a column vector (Nx1) and array2 to be a row vector (1xM)
    diffs = np.abs(frequency_raw[:, np.newaxis] - instrument_array)

    # Find the index of the minimum difference for each element in array1
    idx_min = np.argmin(diffs, axis=1)

    # Use the indices to select the closest values from array2
    rounded_array = instrument_array[idx_min]

    return rounded_array

# Function to apply a fade-in and fade-out to the entire track, accounting for the sample rate
def apply_fade_in_out(audio, fade_duration_ms, sample_rate=44100):
    """
    Apply fade-in at the beginning and fade-out at the end of the audio track.

    Arguments:
    audio -- NumPy array representing the audio data.
    fade_duration_ms -- The duration of the fade-in and fade-out in milliseconds.
    sample_rate -- The sample rate of the audio (e.g., 44100 for CD-quality).

    Returns:
    The audio array with fade-in and fade-out applied.
    """
    # Convert fade duration from milliseconds to samples
    fade_duration_samples = int(fade_duration_ms * sample_rate / 1000)

    # Ensure the fade duration doesn't exceed the length of the audio
    fade_duration_samples = min(fade_duration_samples, len(audio))

    # Create fade-in and fade-out envelopes (values going from 0 to 1 and 1 to 0, respectively)
    fade_in = np.linspace(0, 1, fade_duration_samples)
    fade_out = np.linspace(1, 0, fade_duration_samples)

    # Convert the audio to float to avoid overflow issues during multiplication
    audio = audio.astype(np.float64)

    # Apply fade-in to the start of the audio
    audio[:fade_duration_samples] *= fade_in

    # Apply fade-out to the end of the audio
    audio[-fade_duration_samples:] *= fade_out

    # Convert the audio back to int16
    return np.int16(audio)

# Generate a piano tone based on a frequency value
# This function creates a sine wave for the piano tone
# Arguments:
#   frequency: the frequency of the note in Hz (e.g., 261.63 for C4)
#   duration_ms: duration of the note in milliseconds
#   sample_rate: number of samples per second (default is 44,100 for CD-quality audio)
def generate_piano_tone(frequency, duration_ms, sample_rate=44100):
    # Create time samples based on the duration and sample rate
    samples = np.linspace(0, duration_ms / 1000, int(sample_rate * (duration_ms / 1000)), False)

    # Generate a sine wave at the given frequency
    waveform = 0.5 * np.sin(2 * np.pi * frequency * samples)

    # Convert the waveform to 16-bit PCM format (audio standard)
    audio_data = np.int16(waveform * 32767)

    return audio_data


# Generate a string tone based on a given frequency value
# This function generates a more complex waveform by combining harmonics
# Arguments:
#   frequency: the frequency of the note in Hz (e.g., 261.63 for C4)
#   duration_ms: duration of the note in milliseconds
#   sample_rate: number of samples per second (default is 44,100 for CD-quality audio)
def generate_string_tone(frequency, duration_ms, sample_rate=44100):
    # Convert duration from milliseconds to seconds for time sample generation
    duration_s = duration_ms / 1000.0

    # Generate time samples based on duration and sample rate
    samples = np.linspace(0, duration_s, int(sample_rate * duration_s), False)

    # Generate the fundamental sine wave (the base frequency)
    fundamental = 0.5 * np.sin(2 * np.pi * frequency * samples)

    # Generate harmonic frequencies (multiples of the base frequency)
    harmonic_2 = 0.25 * np.sin(2 * np.pi * (frequency * 2) * samples)  # Second harmonic (double the frequency)
    harmonic_3 = 0.125 * np.sin(2 * np.pi * (frequency * 3) * samples)  # Third harmonic (triple the frequency)

    # Combine the fundamental and harmonics to create the final waveform
    waveform = fundamental + harmonic_2 + harmonic_3

    # Convert the waveform to 16-bit PCM format (audio standard)
    audio_data = np.int16(waveform * 32767)

    return audio_data


# Generate a sequence of tones based on an array of frequencies
# This function creates a sequence of tones (either piano or string) and applies crossfades between them
# Arguments:
#   frequencies: a list of frequencies for each note in the sequence
#   duration_ms: the duration of each note in milliseconds
#   instrument: a string specifying the instrument ('piano' or 'string')
#   cross_fade_percent: the percentage of the duration to use for the crossfade between notes
#   sample_rate: number of samples per second (default is 44,100 for CD-quality audio)
# Generate a sequence of tones based on frequencies array
def generate_tones(frequencies, duration_ms, instrument, cross_fade_percent, sample_rate=44100):
    # Calculate the crossfade duration in milliseconds based on the percentage provided
    transition_ms = duration_ms * cross_fade_percent

    # Calculate the number of samples for each tone and for the transitions
    tone_samples = int(sample_rate * (duration_ms / 1000))
    fade_samples = int(sample_rate * (transition_ms / 1000))

    # Calculate the total length of the combined audio array
    total_samples = len(frequencies) * tone_samples - (len(frequencies) - 1) * fade_samples
    combined_audio = np.zeros(total_samples, dtype=np.int16)

    # Loop over each frequency and generate the corresponding tone
    for i, freq in enumerate(frequencies):
        # Select the instrument and generate the tone
        if instrument == 'piano':
            # Generate a piano tone for the current frequency
            tone = generate_piano_tone(freq, duration_ms, sample_rate)
        elif instrument == 'string':
            # Always generate a new string tone for the current frequency
            tone = generate_string_tone(freq, duration_ms, sample_rate)

        # Calculate the start position for placing the current tone in the combined audio
        start_pos = i * (tone_samples - fade_samples)

        # Apply crossfade if this is not the first tone and if there's enough room for crossfade
        if i > 0 and start_pos >= fade_samples:
            # Determine the number of samples to overlap for the crossfade
            overlap = fade_samples

            # Create fade-in and fade-out arrays for the crossfade
            fade_in = np.linspace(0, 1, overlap)  # Fade in for the current tone
            fade_out = np.linspace(1, 0, overlap)  # Fade out for the previous tone

            # Apply the crossfade to the overlapping region between the previous and current tones
            combined_audio[start_pos - overlap:start_pos] = (
                fade_out * combined_audio[start_pos - overlap:start_pos] +  # Fade out the previous tone
                fade_in * tone[:overlap]  # Fade in the current tone
            ).astype(np.int16)

            # Place the remainder of the current tone (after the crossfade region) in the combined audio array
            combined_audio[start_pos:start_pos + (tone_samples - overlap)] = tone[overlap:]
        else:
            # If this is the first tone or no room for crossfade, place the tone directly
            combined_audio[start_pos:start_pos + tone_samples] = tone

    fade_duration_ms = 100  # 100ms fade duration for both fade-in and fade-out
    fade_duration_samples = int(fade_duration_ms * sample_rate / 1000)

    # Apply a fade-out to the last portion of the combined audio
    combined_audio = apply_fade_in_out(combined_audio, fade_duration_samples)

    # Return the final combined audio array containing all the tones with crossfades
    return combined_audio

# convert audio_data from generate_track or generate_tone into a mp3
def save_as_mp3(audio_data, sample_rate, file_name='output.mp3'):
    # Create a pydub AudioSegment object from the raw audio data
    audio_segment = AudioSegment(
        audio_data.tobytes(),
        frame_rate=sample_rate,
        sample_width=audio_data.dtype.itemsize,
        channels=1
    )
    # Export the audio segment to an MP3 file
    audio_segment.export(file_name, format="mp3")