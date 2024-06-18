from time import*
import cv2
import sys
import json
import base64
import numpy as np
from PySide6.QtGui import QGuiApplication,QImage
from PySide6.QtCore import QObject,Signal,Slot,QProcess,QTimer,Qt,QByteArray,QBuffer,QIODevice
import matplotlib.pyplot as plt
cSA1=1
cSA2=50
gamma=0.08
class ImgProcess:
    def __init__(self,img):
        self.img=img
        self.h,self.w=img.shape
    def rotateImage(self,img,angle)->cv2.typing.MatLike:#通过warpAffine旋转(老朋友了)
        h,w=self.h,self.w
        center=(w//2, h//2) #旋转中心
        scale=1.0 #缩放因子
        anchor=cv2.getRotationMatrix2D(center, angle, scale)
        img=cv2.warpAffine(img, anchor, (w, h))
        return img
    def StartProcess(self):
        img=self.img
        imgN=np.zeros_like(img)
        imgN3=np.zeros_like(img)
        img=cv2.convertScaleAbs(img,alpha=cSA1)
        cv2.imshow("img",img)
        cv2.waitKey(0)
###################################################################################################################################################################################################################
        mList=[]
        for i in range(-50,51):
            imgR=self.rotateImage(img,i/10)
            hList=[]
            for i in range(self.h-2):
                hList.append(np.sum(imgR[i:i+2,:]))#200
            changeH=np.int_(np.diff(hList))
            mList.append(max(changeH))
        self.rotateImage(img,(-50+mList.index(max(mList)))/10)
        wList=[]
        hList=[]
        for i in range(self.h-2):
            hList.append(np.sum(img[i:i+2,:]))#200
        for i in range(self.w-2):
            wList.append(np.sum(img[:,i:i+2]))#200
        hList=np.array(hList)
        wList=np.array(wList)
        changeH=np.int_(np.diff(hList))
        changeW=np.int_(np.diff(wList))
        # 设置坐标轴标签
        hList2=np.linspace(0,len(hList),len(hList)-1)
        wList2=np.linspace(0,len(wList),len(wList)-1)
        # 显示图形
        plt.bar(hList2,np.abs(changeH))
        plt.show()
        plt.bar(wList2,np.abs(changeW))
        plt.show()
        yuZhi=int(input("请输入阈值："))
        changePointH=np.where(np.abs(changeH)>yuZhi)[0]+1
        changePointW=np.where(np.abs(changeW)>yuZhi)[0]+1
        # 列表长度
        ChangesH=changePointH[(changePointH>1)]
        ChangesW=changePointW[(changePointW>1)]
        for i in range(len(ChangesH)-1):
            frontChangesH=ChangesH[0:i]
            if ChangesH[i+1]-ChangesH[i]>100:
                break
        for i in range(len(ChangesH)-1,0,-1):
            backChangesH=ChangesH[i:]
            if ChangesH[i]-ChangesH[i-1]>100:
                break
        for i in range(len(ChangesW)-1):
            frontChangesW=ChangesW[0:i]
            if ChangesW[i+1]-ChangesW[i]>100:
                break
        for i in range(len(ChangesW)-1,0,-1):
            backChangesW=ChangesW[i:]
            if ChangesW[i]-ChangesW[i-1]>100:
                break
        print("前部分的突变点:", frontChangesH)
        print("后部分的突变点:", backChangesH)
        print("前部分的突变点:", frontChangesW)
        print("后部分的突变点:", backChangesW)
        frontChangesH=np.linspace(min(frontChangesH),max(frontChangesH),max(frontChangesH)-min(frontChangesH)+1)
        backChangesH=np.linspace(min(backChangesH),max(backChangesH),max(backChangesH)-min(backChangesH)+1)
        frontChangesW=np.linspace(min(frontChangesW),max(frontChangesW),max(frontChangesW)-min(frontChangesW)+1)
        backChangesW=np.linspace(min(backChangesW),max(backChangesW),max(backChangesW)-min(backChangesW)+1)
        for i in range(self.h):
            for j in range(self.w):
                if i in frontChangesH.tolist()+backChangesH.tolist() and j in frontChangesW.tolist()+backChangesW.tolist():
                    imgN[i,j]=255
###################################################################################################################################################################################################################
        lock=0
        for i in range(self.h):
            for j in range(self.w):
                if j<=self.w-2:
                    if abs(int(imgN[i,j+1])-int(imgN[i,j]))==255 or abs(int(imgN[i,j+1])-int(imgN[i,j]))==5:
                        lock+=1
                if lock/2%2!=0:
                    imgN[i,j]=250 if imgN[i,j]==0 else imgN[i,j]
        imgN=cv2.rotate(imgN,cv2.ROTATE_90_CLOCKWISE)
        for i in range(self.w):
            for j in range(self.h):
                if j<=self.h-2:
                    if abs(int(imgN[i,j+1])-int(imgN[i,j]))==255 or abs(int(imgN[i,j+1])-int(imgN[i,j]))==5:
                        lock+=1
                if lock/2%2!=0:
                    imgN[i,j]=250 if imgN[i,j]==0 else imgN[i,j]
        imgN=cv2.rotate(imgN,cv2.ROTATE_90_COUNTERCLOCKWISE)
        imgN3[imgN>0]=img[imgN>0]
        invGamma=1.0/gamma
        table=(255*np.power(np.arange(0,256.0,1.0)/255.0,invGamma)).astype(np.uint8)
        imgN3=cv2.LUT(imgN3, table)
        imgN3=cv2.convertScaleAbs(imgN3,alpha=cSA2)
        clahe=cv2.createCLAHE(clipLimit=2.0,tileGridSize=(8,8))
        imgN3=clahe.apply(imgN3)
        cv2.imwrite("res\image\output\\14.bmp",imgN3)
        cv2.imshow("33",imgN3)
        cv2.waitKey(0)
if __name__=="__main__":
    img=cv2.imread("E:\PysideGUI\PyUMode\\res\image\input\\1212.bmp",cv2.IMREAD_GRAYSCALE)
    ImgProcess(img).StartProcess()
