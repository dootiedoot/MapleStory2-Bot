import time
import ctypes
from directkeys import PressKey, W, A, S, D, C

user32 = ctypes.windll.user32

for i in list(range(4))[::-1]:
    print(i+1)
    time.sleep(1)

count = 0
while True:

    print("pressed", count)
    PressKey(C)

    user32.keybd_event(0x12, 0, 0, 0)  # Alt
    time.sleep(1)
    user32.keybd_event(0x09, 0, 0, 0)  # Tab
    time.sleep(1)
    user32.keybd_event(0x09, 0, 2, 0)  # ~Tab
    time.sleep(0.1)
    user32.keybd_event(0x12, 0, 2, 0) # ~Alt
    
    time.sleep(1)
    count += 1