import numpy as np
import threading
import cv2
class image_pro:
    def __init__(self,img,numin,numax):
        self.img_data=[img,numin,numax]
    def image_rap(self):
        imgdata = self.img_data
        _,img=cv2.threshold(imgdata[0],imgdata[2]//2.5,imgdata[2],cv2.THRESH_OTSU)
        return img
if __name__ == '__main__':
    weight=0
    img = cv2.imread('res/image/2.bmp',cv2.IMREAD_GRAYSCALE)
    numax=np.max(img)
    numin=np.min(img)
    Image_pro=image_pro(img,numin,numax)
    img=Image_pro.image_rap()
    cv2.imshow('image',img)
    cv2.waitKey(0)