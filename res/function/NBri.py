import numpy as np
import cv2
class image_pro:
    def __init__(self,img):
        self.img=img
    def image_rap(self,value1):
        img = cv2.imread(self.img)
        return img
    
if __name__ == '__main__':
    weight=0
    Image_pro=image_pro('res/image/photos.bmp')
    img=Image_pro.image_rap(weight)
    cv2.imshow('image',img)
    cv2.waitKey(0)