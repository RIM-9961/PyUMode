from time import*
import cv2
import numpy as np
class ImgProcess:
    def __init__(self,img):
        self.img=img
        self.x,self.y=img.shape
    def StartProcess(self):
        img=self.img
        imgN=np.zeros_like(img)
        imgN2=np.zeros_like(img)
        imgN3=np.zeros_like(img)
        imgN4=np.zeros_like(img)
        img=np.uint8(cv2.addWeighted(img,5,img,0,0))
        img=cv2.fastNlMeansDenoising(img,dst=None,h=200,templateWindowSize=2,searchWindowSize=7)
        img=img/255
        cK=np.array([[-1,-1,-1],[-1, 8,-1],[-1,-1,-1]])
        imgL=cv2.filter2D(img,-1,cK*5) #滤波
        img+=imgL*2
        img=np.where(img>1,1,img)
        img=cv2.fastNlMeansDenoising(np.uint8(np.abs(img)*255),dst=None,h=200,templateWindowSize=5,searchWindowSize=5)
        imgN4=cv2.threshold(img,200,255,cv2.THRESH_BINARY)[1]
        contours=cv2.findContours(imgN4,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[0]
        areaList=[cv2.contourArea(contour) for contour in contours]
        imgN4=np.zeros_like(imgN4)
        cv2.drawContours(imgN4,[contours[areaList.index(max(areaList))]],-1,(255,255,255),-1)
        img[imgN4>0]=imgN[imgN4>0]
        for i in range(self.x):
            num=np.sum(img[i,:]>=200)
            if num>=600:
                imgN[i,:]=img[i,:]
        for i in range(self.y):
            num=np.sum(img[:,i]>=200)
            if num>=300:
                for j in range(1,self.x-1):
                    if imgN[j,i]>0:
                        imgN2[j,i]=imgN[j,i]
        imgN2=np.where(imgN2>0,255,imgN2)
        lock=0
        for i in range(self.x):
            for j in range(self.y):
                if j<=self.y-2:
                    if imgN2[i,j]==255 and imgN2[i,j+1]!=255:
                        lock+=1
                if lock%2!=0:
                    imgN2[i,j]=250
        imgN2=cv2.rotate(imgN2,cv2.ROTATE_90_CLOCKWISE)
        for i in range(self.y):
            for j in range(self.x):
                if j<=self.y-2:
                    if imgN2[i,j]==255 and imgN2[i,j+1]!=255:
                        lock+=1
                if lock%2!=0:
                    imgN2[i,j]=250
        imgN2=cv2.rotate(imgN2,cv2.ROTATE_90_COUNTERCLOCKWISE)
        imgN3[imgN2>0]=img[imgN2>0]
        #imgN3=cv2.equalizeHist(imgN3)
        #imgN3=np.where(imgN3>=2,255,imgN3)
        #gamma=3  # Gamma值小于1会使图像变亮
        #invGamma=1.0/gamma
        #table=(255*np.power(np.arange(0,256.0,1.0)/255.0,invGamma)).astype(np.uint8)
        #imgN3=cv2.LUT(imgN3, table)
        #imgN3=cv2.threshold(imgN3,120,255,cv2.THRESH_BINARY)[1]
        cv2.imshow("img",imgN3)
        cv2.waitKey(0)
        cv2.imwrite("res\image\output\\13.bmp",imgN3)
if __name__=="__main__":
    img=cv2.imread("res\image\input\\13.bmp",cv2.IMREAD_GRAYSCALE)
    ImgProcess(img).StartProcess()
#img=cv2.medianBlur(self.img,5)#模糊