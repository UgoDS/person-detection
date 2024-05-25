import cv2
import numpy
import time
from datetime import datetime
import glob
import os

import mss

from alert import send_email
from detection import detect_humans_yolov3

# Remove images before starting
list_images = glob.glob("screenshots/raw/frame_*.jpeg")
_ = [os.remove(img) for img in list_images]


with mss.mss() as sct:
    # Part of the screen to capture
    monitor = {"top": 40, "left": 0, "width": 800, "height": 640}

    while "Screen capturing":
        # 1 fps
        time.sleep(1)

        # Get raw pixels from the screen, save it to a Numpy array
        frame = numpy.array(sct.grab(monitor))

        # Display the picture
        img_path = f'screenshots/raw/frame_{datetime.now().strftime("%Y%m%d_%H%M%S")}.jpeg'
        cv2.imwrite(
            img_path,
            frame,
        )
        output_path = detect_humans_yolov3(img_path)
        send_email(output_path)
        list_images = glob.glob("screenshots/raw/frame_*.jpeg")
        if len(list_images) >= 10:
            os.remove(list_images[0])
        # Press "q" to quit
        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break
