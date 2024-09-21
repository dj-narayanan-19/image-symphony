from extractHorizon import *
from audioProcessing import *
from createVideo import *
from buildMovie import *
import os
from layer_tracks import layer_tracks
from book_keeping import *

def run_script(image_name, true_time, instrument_array, delay_vector, continuation_prompt, threshold = 0.3, cross_percentage = 0.5, scaling_factor = 1.):
    # calculate some consistent variables
    total_time = true_time - max(delay_vector)

    # instrument arrays
    # Define the common range using generate_frequencies function
    # Violin: G3 (196 Hz) to E6 (1318 Hz), roughly 3 octaves
    violin_common = generate_frequencies(196, 3)  # G3 to E6
    # Viola: C3 (130.81 Hz) to A5 (880 Hz), roughly 2.5 octaves
    viola_common = generate_frequencies(130.81, 2.5)  # C3 to A5
    # Cello: C2 (65.41 Hz) to A4 (440 Hz), roughly 3 octaves
    cello_common = generate_frequencies(65.41, 3)  # C2 to A4
    # Double Bass: E1 (41.20 Hz) to G3 (196 Hz), roughly 2 octaves
    bass_common = generate_frequencies(41.20, 2)  # E1 to G3
    # Piano: A1 (55 Hz) to C6 (1046.5 Hz), roughly 5 octaves
    piano_common = generate_frequencies(55, 5)  # A1 to C6
    # Violin: G3 (196 Hz) to E7 (~2637 Hz)
    violin_full = generate_frequencies(196, 4)  # G3 to E7
    # Viola: C3 (130.81 Hz) to A6 (~1760 Hz)
    viola_full = generate_frequencies(130.81, 4)  # C3 to A6
    # Cello: C2 (65.41 Hz) to A5 (~880 Hz)
    cello_full = generate_frequencies(65.41, 4)  # C2 to A5
    # Double Bass: E1 (41.20 Hz) to G4 (~392 Hz)
    bass_full = generate_frequencies(41.20, 3)  # E1 to G4
    # Piano: A0 (27.5 Hz) to C8 (~4186 Hz)
    piano_full = generate_frequencies(27.5, 7)  # A0 to C8

    # define paths for saving
    source_path, destination_path = create_paths(image_name)
    destination_path = exe_path(image_name)

    # get the horizon
    img, imgRGB = import_and_preprocess(source_path, scaling_factor)
    height, width = img.shape[:2]
    gray = convert_to_binary_image(img, threshold=threshold)
    horizon = threshold_horizon(gray)
    print('horizon extracted')

    ask_about_horizon(img, horizon, continuation_prompt)

    tone_duration = (total_time * 1000) / (width * (1 - cross_percentage))
    print('tone duration is: ', tone_duration)
    print('time of video is : ', true_time)

    # -----VIZ-------
    animate_horizontal_bars_with_delay(imgRGB, horizon, total_time, bar_thickness=2, bar_delay=delay_vector, output_file='output/output_video.mp4')
    print('video created')

    # -----AUDIO-------
    combined_audios = [None]*len(delay_vector)

    # converts user string input to array variables


    instrument_array_tones = [locals()[var_name] for var_name in instrument_array]
    counter = 0
    # iterate through instrument array and assign the track to combined_audios
    for instrument in instrument_array_tones:
        frequency = instrument_frequency(horizon, instrument)
        output_track = generate_tones(frequency, duration_ms=tone_duration, instrument='string', cross_fade_percent=cross_percentage)
        combined_audios[counter] = output_track
        counter = counter+1
        print('audio track ', counter, ' created')

    audio_output = layer_tracks(combined_audios, delay_vector)
    print('final track created')
    save_as_mp3(audio_output, sample_rate=44100, file_name='output/output_audio.mp3')


    # -----COMBINATION-----
    combine_audio_video('output/output_video.mp4', 'output/output_audio.mp3', output_path=destination_path)



#run_script('mountain_jungle.jpeg', 60, threshold=0.53, instrument_array = ['viola', 'piano_small', 'piano_medium'], delay_vector = [0, 10, 20], cross_percentage=0.75, scaling_factor=0.2)

