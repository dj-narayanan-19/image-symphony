from extractHorizon import *
from audioProcessing import *
from createVideo import *
from buildMovie import *
import os
import sys
from layer_tracks import layer_tracks
import tkinter as tk
from tkinter import filedialog, messagebox

def create_paths(image_name, source_folder = 'test_images', destination_folder = 'combined_videos'):
    base_name = os.path.splitext(image_name)[0]  # This will remove the original extension
    new_file_name = base_name + '.mp4'  # Add the .mp4 extension
    source_path = os.path.join(source_folder, image_name)
    destination_path = os.path.join(destination_folder, new_file_name)

    return source_path, destination_path

def exe_path(image_name):
    if getattr(sys, 'frozen', False):
        # If running from a PyInstaller bundle
        base_path = sys._MEIPASS  # Extracts temporary directory used by PyInstaller
    else:
        # Normal case when running from source
        base_path = os.path.dirname(os.path.abspath(__file__))
    base_name = os.path.splitext(image_name)[0]  # This will remove the original extension
    new_file_name = base_name + '.mp4'  # Add the .mp4 extension

    # Example: Create an "output" folder in the executable's directory
    output_folder = os.path.join(base_path, 'output')
    destination_path = os.path.join(output_folder, new_file_name)

    # Create the directory if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    return destination_path

def create_mp3_track(horizon, instrument_array, tone_duration_ms, cross, instrument):
    frequency = instrument_frequency(horizon, instrument_array)
    output_track = generate_tones(frequency, duration_ms=tone_duration_ms, instrument=instrument, cross_fade_percent=cross)

    return output_track


def ask_about_horizon(img_horizon, horizon, continuation_prompt):
    # draw red circles on the horizon
    for x in range(img_horizon.shape[1]):
        cv2.circle(img_horizon, (x, horizon[x]), 1, (0, 0, 255), -1)
    # save horizon image
    cv2.imwrite('debugImages/horizon_img.jpg', img_horizon)

    # show horizon image
    cv2.imshow('Horizon preview', img_horizon)
    cv2.waitKey(1)

    # Instead of input(), use the provided continuation prompt function
    if not continuation_prompt():
        print("Process stopped by user.")
        cv2.destroyAllWindows()
        sys.exit()


    # Continue processing if the user chose to continue
    print("Continuing process...")
    # Further processing logic here
    cv2.destroyAllWindows()

    '''
    # Ask the user for confirmation
    response = input("Is the desired horizon (yes/no): ").strip().lower()
    if response in ['yes', 'y']:
        print("Proceeding...")
        return True
    elif response in ['no', 'n']:
        print("Exiting...")
        sys.exit()  # Exit the script if the user is not satisfied
    else:
        print("Invalid response. Exiting...")
        sys.exit()
    '''

'''
#----user-defined----
#tone_duration = 200
total_time = 120
cross_percentage = 0.5
threshold = 0.3
image_name = 'boats.jpeg'
scaling_factor = 2
width = 600*scaling_factor
height = 400*scaling_factor
delay_vector = [0, 15, 30]
true_time = total_time+max(delay_vector)


tone_duration = (total_time*1000)/(width * (1 - cross_percentage))
print('tone duration is: ', tone_duration)
print('time of video is : ', true_time)


# instrument arrays
viola = np.array([130.8128, 195.9977, 293.6648, 440])
piano = np.array([  27.5       ,   29.13523509,   30.86770633,   32.70319566,
         34.64782887,   36.70809599,   38.89087297,   41.20344461,
         43.65352893,   46.24930284,   48.9994295 ,   51.9130872 ,
         55.        ,   58.27047019,   61.73541266,   65.40639133,
         69.29565774,   73.41619198,   77.78174593,   82.40688923,
         87.30705786,   92.49860568,   97.998859  ,  103.82617439,
        110.        ,  116.54094038,  123.47082531,  130.81278265,
        138.59131549,  146.83238396,  155.56349186,  164.81377846,
        174.61411572,  184.99721136,  195.99771799,  207.65234879,
        220.        ,  233.08188076,  246.94165063,  261.6255653 ,
        277.18263098,  293.66476792,  311.12698372,  329.62755691,
        349.22823143,  369.99442271,  391.99543598,  415.30469758,
        440.        ,  466.16376152,  493.88330126,  523.2511306 ,
        554.36526195,  587.32953583,  622.25396744,  659.25511383,
        698.45646287,  739.98884542,  783.99087196,  830.60939516,
        ])
piano_medium = np.array([58.27047019,   61.73541266,   65.40639133,
         69.29565774,   73.41619198,   77.78174593,   82.40688923,
         87.30705786,   92.49860568,   97.998859  ,  103.82617439,
        110.        ,  116.54094038,  123.47082531,  130.81278265,
        138.59131549,  146.83238396,  155.56349186,  164.81377846,
        174.61411572,  184.99721136,  195.99771799,  207.65234879,
        220.        ,  233.08188076,  246.94165063,  261.6255653 ,
        277.18263098,  293.66476792,  311.12698372,  329.62755691,
        349.22823143,  369.99442271,  391.99543598,  415.30469758,
        440.        ,  466.16376152,  493.88330126,  523.2511306 ,
        554.36526195,  587.32953583,  ])
piano_small = np.array([110.        ,  116.54094038,  123.47082531,  130.81278265,
        138.59131549,  146.83238396,  155.56349186,  164.81377846,
        174.61411572,  184.99721136,  195.99771799,  207.65234879,
        220.        ,  233.08188076,  246.94165063,  261.6255653 ,
        277.18263098,  293.66476792,  311.12698372,  329.62755691,
        349.22823143,  369.99442271,  391.99543598,  415.30469758,])

# define paths for saving
source_path, destination_path = create_paths(image_name)

#get the horizon
img, imgRGB = import_and_preprocess(source_path, width, height)
gray = convert_to_binary_image(img, threshold=threshold)
horizon = threshold_horizon(gray)

#-----VIZ-------
animate_horizontal_bars_with_delay(imgRGB, horizon, total_time, bar_thickness= 2, bar_delay= delay_vector, output_file='debug_av/output_video.mp4')

#-----AUDIO-------
# create viola track
frequency1 = instrument_frequency(horizon, piano_small)
output_track1 = generate_tones(frequency1, duration_ms=tone_duration, instrument='piano', cross_fade_percent=cross_percentage)
print('track1 created')

frequency2 = instrument_frequency(horizon, piano_medium)
output_track2 = generate_tones(frequency2, duration_ms=tone_duration, instrument='piano', cross_fade_percent=cross_percentage)
print('track2 created')

frequency3 = instrument_frequency(horizon, piano)
output_track3 = generate_tones(frequency3, duration_ms=tone_duration, instrument='piano', cross_fade_percent=cross_percentage)
print('track3 created')

audio_output = layer_tracks([output_track1, output_track2, output_track3], delay_vector)

save_as_mp3(audio_output, 44100, file_name='debug_av/output_audio.mp3')

#-----COMBINATION-----
combine_audio_video('debug_av/output_video.mp4', 'debug_av/output_audio.mp3', output_path=destination_path)



the end result on audio --> 

you give it
---- image
---- [an array of instruments] # eg. ['viola', 'piano']
---- [delay_vector] # the times those instruments come in, [0, 5]
---- [the length of the video you want [default a 90 seconds]]

it gives you
--- final video with those properties
'''
