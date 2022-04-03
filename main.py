import os

import cv2 as cv
import numpy as np
from datetime import date
import platform
from appscript import app, mactypes
import subprocess
from wallpaper import set_wallpaper

height = 1800
width = 2880
image = np.zeros((height, width, 3), np.uint8)


def setup_image_wallpaper(image):
    d0 = date.today()
    if "date_file.txt" not in os.listdir():
        f = open("date_file.txt", "w")
        f.write(input("Enter date (dd/mm/yy) eg for 5th January 2022: (05/01/22)-> "))
        f.close()
    f = open("date_file.txt", "r")
    data = f.read()
    f.close()
    data = data.split("/")
    d1 = date(int(data[0]), int(data[1]), 2000 + int(data[2]))
    delta = d1 - d0
    text = str(delta.days) + " Days left!"
    h, w, c = image.shape
    thickness = 5
    cv.putText(image, str(text), (w // 2 - 100, h // 2 - 100), cv.FONT_HERSHEY_SIMPLEX, thickness, (255, 255, 255), 4)
    return image, delta
    # cv.imshow("test", image)
    # if cv.waitKey(0) & 0xff == ord('q'):
    #     cv.destroyAllWindows()
    #     return "b"


def save_image(image, days):
    cv.imwrite("Wallpaper{days}.png".format(days=str(days)), image)
    if "Wallpaper{days}.png".format(days=days) in os.listdir():
        return os.getcwd() + "/Wallpaper{days}.png".format(days=days)
    else:
        raise Exception("Failed to find wallpaper!")


def setting_wallpaper(path):
    # SCRIPT = """/usr/bin/osascript<<END
    # # tell application "Finder"
    # # set desktop picture to POSIX file "%s"
    # # end tell
    # END"""
    if platform.system() == "Darwin":
        SCRIPT = """/usr/bin/osascript<<END
        tell application "System Events"
        tell current desktop
            set picture rotation to 0
            set picture to "{PATH}"
        end tell
    end tell 
        END"""
        subprocess.Popen(SCRIPT.format(PATH=path), shell=True)
    elif platform.system() == "Linux":
        set_wallpaper(path)


a, delta = setup_image_wallpaper(image=image)
text = save_image(a, delta.days)
setting_wallpaper()