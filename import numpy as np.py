import os
import openai
openai.organization = "org-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"
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.Model.list()
import numpy as np
import cv2
import pyautogui
import model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=False, progress=True, pretrained_backbone=True)

# initialize the NVIDIA 20 series graphics card
graphics_card = cv2.VideoCapture(0)

while True:
    # capture the image from the graphics card
    ret, frame = graphics_card.read()
    if not ret:
        print("Error capturing video frame.")
        break

    # convert the image to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # load the Fortnite character template
    fortnite_template = cv2.imread('fortnite_character.jpg', 0)

    # match the template with the image
    result = cv2.matchTemplate(gray, fortnite_template, cv2.TM_CCOEFF_NORMED)

    # get the confidence strength
    confidence_strength = np.amax(result)

    # get the coordinates of the character
    loc = np.where(result >= confidence_strength)

    # get the coordinates of the character
    for pt in zip(*loc[::-1]):
        # get the distance of the character
        distance = np.sqrt((pt[0] - frame.shape[1]/2) **
                           2 + (pt[1] - frame.shape[0]/2)**2)

        # adjust the interpolation fps
        interpolation_fps = distance/100

        # move the mouse to the character
        pyautogui.moveTo(pt[0], pt[1], interpolation_fps)
