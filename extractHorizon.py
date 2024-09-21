import cv2
import numpy as np
from pydub import AudioSegment


# take image and convert it to boosted black and white
def import_and_preprocess(image_path, scaling_factor):
    # Step 1: Load the image
    image = cv2.imread(image_path)
    height, width = image.shape[:2]
    height = int(height * scaling_factor)
    width = int(width * scaling_factor)

    img_size = (width, height)
    if width != 0:
        image = cv2.resize(image, (img_size[0], img_size[1]), interpolation=cv2.INTER_AREA)
    imgRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    return image, imgRGB

def convert_to_binary_image(img, threshold = 0.5):
    # Step 2: Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite('debugImages/gray.jpg', gray)
    print(f"Threshold value: {threshold}, type: {type(threshold)}")
    _, binary_image = cv2.threshold(gray, 255*threshold, 255, cv2.THRESH_BINARY_INV)

    # cv2.imwrite('debugImages/gray.jpg', gray)
    # cv2.imwrite('debugImages/gray_contrast.jpg', binary_image)

    post_process = binary_image.copy()

    return post_process

# find the horizon array
def threshold_horizon(img):
    horizon = np.zeros(img.shape[1], dtype = int)

    # Iterate through each column (x-coordinate)
    for x in range(img.shape[1]):
        # Iterate through each row (y-coordinate) from top to bottom to find the transition
        for y in range(img.shape[0]):
            if img[y, x] > 0:
                horizon[x] = y
                break

    # potentially put smoothing in here

    # viz
    #img_horizon = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    #for x in range(img.shape[1]):
    #    cv2.circle(img_horizon, (x, horizon[x]), 1, (0, 0, 255), -1)

    #cv2.imwrite('debugImages/horizon_img.jpg', img_horizon)
    #cv2.imshow('Horizon', img_horizon)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    return horizon.astype(int)

# map horizon array to a frequency range
def map_horizon(array, old_min, old_max, new_min, new_max):
    mapped_array = new_max - (array/old_max)*(new_max - new_min)
    return mapped_array.astype(int)

