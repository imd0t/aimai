import numpy as np
import cv2
import pyautogui
from queue import PriorityQueue
from keyboard import is_pressed

# Initialize the NVIDIA 20 series graphics card
graphics_card = cv2.VideoCapture(0)

# Parameters
interpolation_fps = "unlimited"
confidence_threshold = 0.5
strength = 1.0
aiming_down_sights = False
hipfire = True

# Function keys
function_key_1 = False
function_key_2 = False

while True:
    # Check function key status
    function_key_1 = is_pressed('f1')
    function_key_2 = is_pressed('f2')

    if function_key_1:
        aiming_down_sights = not aiming_down_sights
        hipfire = not hipfire

    # Capture the image from the graphics card
    ret, frame = graphics_card.read()
    if not ret:
        print("Error capturing video frame.")
        break

    # Convert the image to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Load the Fortnite character template
    fortnite_template = cv2.imread('fortnite_character.jpg', 0)

    # Match the template with the image
    result = cv2.matchTemplate(gray, fortnite_template, cv2.TM_CCOEFF_NORMED)

    # Get the confidence strength
    confidence_strength = np.amax(result)

    if confidence_strength >= confidence_threshold and function_key_2:
        # Get the coordinates of the characters
        loc = np.where(result >= confidence_strength)

        # Store characters in a priority queue based on distance
        characters = PriorityQueue()
        for pt in zip(*loc[::-1]):
            # Get the distance of the character
            distance = np.sqrt((pt[0] - frame.shape[1]/2)**2 + (pt[1] - frame.shape[0]/2)**2)
            characters.put((distance, pt))

        # Get the second furthest character
        if characters.qsize() >= 2:
            characters.get()
            second_furthest = characters.get()[1]

            # Adjust the interpolation fps
            if interpolation_fps != "unlimited":
                interpolation_fps = distance/100

            # Move the mouse to the character
            if aiming_down_sights:
                pyautogui.moveTo(second_furthest[0], second_furthest[1], interpolation_fps, _pause=False)
            elif hipfire:
                pyautogui.moveRel(second_furthest[0] * strength, second_furthest[1] * strength, _pause=False)

graphics_card.release()
cv2.destroyAllWindows()
