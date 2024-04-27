c=b'555'
print(c,c.decode("gbk"))
'''import cv2
import numpy as np
class img_process:
    def __init__(self,img):
        self.img=img.astype(float)
        self.imgzero=np.zeros_like(img)
    def CleanZaoDian(self):
        yI,xI=np.shape(self.img)
        for r in range(xI//2+100,400,-1):
            img_CZD=np.zeros_like(self.img)
            text=np.zeros_like(self.img)
            cv2.circle(img_CZD,(int(xI/2),int(yI/2)),r,(255,0,0),3)
            self.imgzero=img_CZD+self.img+self.imgzero
            text=img_CZD+self.img
            text=np.where(text<=360,0,text)
            self.imgzero=np.where(self.imgzero<=360,0,self.imgzero)
            cv2.imshow("0",self.imgzero)
            cv2.waitKey(10)
        self.imgzero=np.where(self.imgzero>360,255,self.imgzero)
        cv2.imshow("ZaoDian",img)
        cv2.waitKey(0)
        cv2.imshow("CleanZaoDian",self.imgzero)
        cv2.waitKey(0)
if __name__ == '__main__':
    img=cv2.imread("res\image\photos.bmp")
    img=cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    _,Th_img=cv2.threshold(img,100,255,cv2.THRESH_BINARY)
    cv2.imshow("img",Th_img)
    cv2.waitKey(0)
    #img_process(img).CleanZaoDian()'''