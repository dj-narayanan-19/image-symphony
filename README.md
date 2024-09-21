This is a project i've done based on this: https://wernerdevalk.nl/en/songs-of-the-horizon/ 
All credit there for the original idea

To run:
1. run create_UI.py
2. Select your image and adjust parameters (if they're not self-explanatory, ask me what it means)It
3. After completing the run it should generate a video with audio based on the height of the horizon at each point


Example: https://youtu.be/vRM_7F1VZ04

-------------------------------

Required python libraries:
- sys
- json
- os
- opencv
- numpy
- pydub
- moviepy
- matplotlib

This command should work to install them (if not, idk ask chatGPT)

pip install opencv-python numpy pydub moviepy matplotlib


--------------------------------------

Example: https://youtu.be/vRM_7F1VZ04

Uses the following config:

{
"image_file": "/Users/dhananjaynarayanan/PycharmProjects/extractHorizon/test_images/mountain_jungle.jpeg", 

"true_time": 60, 

"threshold": 0.53, 

"instrument_array": "piano_common, violin_common, viola_full", 

"delay_vector": "0, 5, 10", 

"cross_percentage": 0.75, 

"scaling_factor": 0.2}
