from time import*
import cv2
import sys
import json
import base64
import numpy as np
from PySide6.QtGui import QGuiApplication,QImage
from PySide6.QtCore import QObject,Signal,Slot,QProcess,QTimer,Qt,QByteArray,QBuffer,QIODevice
imgPath=sys.argv[1]
with open(imgPath,'r') as f:
    imgList = f.read()
    if imgList is not None:
        imgList=json.loads(imgList)
decodedBytes=base64.b64decode(imgList[0])#上面是将base64编码的图像数据从QByteArray通过base64解码读取转换为Bytes
nparr=np.frombuffer(decodedBytes,np.uint8)  
img=cv2.imdecode(nparr,cv2.IMREAD_GRAYSCALE)#传输的图像
###########################################################################################################################################################################
###########################################################################################################################################################################
PImage=QImage(img.data,img.shape[1],img.shape[0],img.strides[0],QImage.Format_Grayscale8)
byteArray=QByteArray()
buffer=QBuffer(byteArray)
buffer.open(QIODevice.WriteOnly)
PImage.save(buffer,"PNG")
img=byteArray.toBase64().data().decode()#将处理过的图像数据转换为base64编码的图像数据
print(img)
sys.stdout.flush()
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
        img=np.uint8(cv2.addWeighted(img,1,img,0,0))
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
###################################################################################################################################################################################################################
        for i in range(self.x):
            num=np.sum(img[i,:]>=170)#200
            if num>=400:#600
                imgN[i,:]=img[i,:]
        for i in range(self.y):
            num=np.sum(img[:,i]>=160)#200
            if num>=300:
                for j in range(1,self.x-1):
                    if imgN[j,i]>0:
                        imgN2[j,i]=imgN[j,i]
        imgN2=np.where(imgN2>0,255,imgN2)
###################################################################################################################################################################################################################
        lock=0
        op=2
        for i in range(self.x):
            for j in range(self.y):
                if j<=self.y-2:
                    if abs(int(imgN2[i,j+1])-int(imgN2[i,j]))==255 or abs(int(imgN2[i,j+1])-int(imgN2[i,j]))==5:
                        lock+=1
                if lock/2%2!=0:
                    if i< self.x//2:
                        imgN2[i:i+op,j]=np.where(imgN2[i:i+op,j]==0,250,imgN2[i:i+op,j])
                    else:
                        imgN2[i-op:i,j]=np.where(imgN2[i-op:i,j]==0,250,imgN2[i-op:i,j])
        imgN2=cv2.rotate(imgN2,cv2.ROTATE_90_CLOCKWISE)
        for i in range(self.y):
            for j in range(self.x):
                if j<=self.x-2:
                    if abs(int(imgN2[i,j+1])-int(imgN2[i,j]))==255 or abs(int(imgN2[i,j+1])-int(imgN2[i,j]))==5:
                        lock+=1
                if lock/2%2!=0:
                    if i< self.x//2:
                        imgN2[i-op:i,j]=np.where(imgN2[i-op:i,j]==0,250,imgN2[i-op:i,j])
                    else:
                        imgN2[i:i+op,j]=np.where(imgN2[i:i+op,j]==0,250,imgN2[i:i+op,j])
        imgN2=cv2.rotate(imgN2,cv2.ROTATE_90_COUNTERCLOCKWISE)
        imgN3[imgN2>0]=img[imgN2>0]
        imgN3=cv2.equalizeHist(imgN3)
        gamma=0.5  # Gamma值小于1会使图像变亮
        invGamma=1.0/gamma
        table=(255*np.power(np.arange(0,256.0,1.0)/255.0,invGamma)).astype(np.uint8)
        imgN3=cv2.LUT(imgN3, table)
        imgN3=cv2.equalizeHist(imgN3)
        #imgN3=cv2.threshold(imgN3,120,255,cv2.THRESH_BINARY)[1]
        print(imgN3)
        sys.stdout.flush()
        cv2.imwrite("res\image\output\\13.bmp",imgN3)
'''if __name__=="__main__":
    img=cv2.imread("res\image\input\\11.bmp",cv2.IMREAD_GRAYSCALE)
    ImgProcess(img).StartProcess()'''
#img=cv2.medianBlur(self.img,5)#模糊