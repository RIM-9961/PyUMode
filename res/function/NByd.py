import cv2
import numpy as np
from opencv_display import *
def main():
    result = cksdk.CameraEnumerateDevice()
    if result[0] != 0:
        print("Don't find camera")
        return
    print("Find cameras number: %d" % result[1])
    opencv_display()

if __name__ == '__main__':
    main()
    print("exit!!!")
    cv2.Canny
