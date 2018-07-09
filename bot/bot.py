from PIL import ImageGrab
from PIL import Image
from grabscreen import grab_screen
from getkeys import key_check
import cv2
import time
import win32gui 
import numpy as np
import pytesseract
import os
import directkeys

def main():
    for i in list(range(3))[::-1]:
        print(i+1)
        time.sleep(1)

    window_name = r'MapleStory2 - A New Beginning'

    hwnd = win32gui.FindWindow(None, window_name)

    last_time = time.time()
    paused = False
    print('STARTING!!!')
    while(True):
        if not paused:
            

            #grabbed_image = cv2.resize(grabbed_image, (640, 360))
            #cv2.imwrite('image.png',grabbed_image)
            #cv2.imshow('window', grabbed_image)
            # resize to something a bit more acceptable for a CNN
            #cv2_image = np.array(grabbed_image.convert('RGB'))

            #grabbed_image.show()
            # screen = grab_screen(window_dimensions)
            # cv2.imshow('MS2', image)
            last_time = time.time()

            #   if active window is our application...
            if win32gui.GetWindowText(win32gui.GetForegroundWindow()) == window_name:
                RGB_image = _get_window_image(hwnd)
                img_HP_bar = _get_HP_bar_image_from_image(RGB_image)
                cv2.imshow("HP Bar", img_HP_bar)
                hp = _get_HP_from_image(img_HP_bar)

                if hp != None:
                    if hp <= 1200:
                        directkeys.PressKey(0x02)
                        time.sleep(.5)
                        directkeys.ReleaseKey(0x02)
                        print("Used potion!")

                # print(hp)
            else:
                print("MS2 is not active window. Doing nothing.")

        #   Press 'T' to pause
        keys = key_check()
        if 'T' in keys:
            if paused:
                paused = False
                print('unpaused!')
                time.sleep(1)
            else:
                print('Pausing!')
                paused = True
                time.sleep(1)

        #   buffer to avoid crashing
        cv2.waitKey(1)

    cv2.destroyAllWindows()
    print("Ended")

#   returns the image of the game given a window
def _get_window_image(window):
        window_dimensions = win32gui.GetWindowRect(window)
        #grabbed_image = grab_screen(region=(0, 40, 1920, 1120))

        grabbed_image = grab_screen(window_dimensions)
        #grabbed_image  = cv2.resize(grabbed_image, (480, 270))

        # run a color convert:
        RGB_image = cv2.cvtColor(grabbed_image, cv2.COLOR_BGR2RGB)
        return RGB_image

#   returns the image of the cropped HP bar given an image of the game
def _get_HP_bar_image_from_image(img):
    height, width, channels = img.shape

    #   [NOTE] configs for HP locations based on resolution and UI scaling
    #   1768 x 992 with 50% UI Scale: x = width/2 - 60, y = height - 120, height = y + 15, width = x + 57

    #   Adjust coordinates to HP bar
    x = int(round((width) / 2 - 60))
    y = int(height - 120)
    height = y + 15
    width = x + 57

    crop_img = img[y:height, x:width]
    return crop_img

#   returns the HP amount in int format given an image of the HP bar
def _get_HP_from_image(img):
    if not img.any():
        print("No HP image found!")
        return

    #   convert to grayscale
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    #   Resize image
    # img = cv2.resize(img, (384, 216), fx=1, fy=1, interpolation = cv2.INTER_CUBIC)
    
    # Apply dilation and erosion to remove some noise
    # kernel = np.ones((1, 1), np.uint8)
    # img = cv2.dilate(img, kernel, iterations=1)
    # img = cv2.erode(img, kernel, iterations=1)

    cv2.imwrite('C:/Users/chadh/Desktop/MS2-Bot/hp2g.png', img)

    #   convert opencv img to Image for pytesseract
    img = Image.fromarray(img)
    hp = pytesseract.image_to_string(img, config='outputbase digits')

    #   attempt to return parsed
    if hp.isdigit():
        return int(hp)
    else:
        return None

main()
# RGB_image = _get_window_image(r'MapleStory2 - A New Beginning')
# img_HP_bar = _get_HP_bar_image_from_image(RGB_image)
# # cv2.imshow("HP Bar", img_HP_bar)
# # hp = _get_HP_from_image(img_HP_bar)
# # print(hp)
# # cv2.imshow("HP Bar", hp_img)
# k = cv2.waitKey(1)
# if k == 27: # wait for ESC key to exit
#     print("Exiting loop")