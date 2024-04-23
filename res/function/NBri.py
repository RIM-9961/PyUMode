import cv2
import time
import numpy as np
#@RIM(这个人写的)->https://github.com/RIM-9961
#让幼儿园大班都能看懂程度的能力
#保姆级代码
class imageProFast:
    def __init__(self,img,numin,numax,yI,xI):#这是注册信息
        self.img_data={"图片矩阵":img,"最小灰度值":numin,"最大灰度值":numax,"图片高度":yI,"图片宽度":xI}
        self.THVMAX=800
        self.THVMIN=10
        self.BLI=2.5
        self.angle=-0.2
    def imageRap(self)->cv2.typing.MatLike:#这是图像require和process操作
        imgdata = self.img_data
        _,img=cv2.threshold(imgdata["图片矩阵"],imgdata["最大灰度值"]//self.BLI,imgdata["最大灰度值"],cv2.THRESH_OTSU)
        img=self.rotateImage(img,self.angle)#旋转图像操作
        _,img=cv2.threshold(img,imgdata["最大灰度值"]//self.BLI,imgdata["最大灰度值"],cv2.THRESH_OTSU)
        img=self.cleanCenter(img)#中心标签去除操作
        img=self.cleanEdge(img)#边缘杂边去除操作
        np.save("res/npy/img.npy",img)
        return img
    def rotateImage(self,img,angle)->cv2.typing.MatLike:#通过warpAffine旋转(老朋友了)
        yI,xI=self.img_data["图片高度"],self.img_data["图片宽度"]
        center = (xI//2, yI//2)  # 旋转中心
        scale = 1.0  # 缩放因子
        anchor = cv2.getRotationMatrix2D(center, angle, scale)
        img = cv2.warpAffine(img, anchor, (xI, yI))
        return img
    def cleanCenter(self,img)-> cv2.typing.MatLike:#不断画圆收缩直至圆轮廓内无0从而去除中心标签
        yI,xI=self.img_data["图片高度"],self.img_data["图片宽度"]
        for r in range(yI//2+100,0,-5):
            img_CZD=np.zeros(img.shape,dtype=np.uint8)
            cv2.circle(img_CZD,(xI//2,yI//2),r,(255,0,0),2)
            if np.all(img[img_CZD==255]==0):
                cv2.circle(img_CZD,(xI//2,yI//2),r,(255,0,0),-1)
                img[img_CZD==255]=0
                return img
    def cleanEdge(self,img)-> cv2.typing.MatLike:#通过遍历横纵坐标完善图像，使边缘更整齐
        lock=False
        for x in range(self.img_data["图片宽度"]):
            num=np.count_nonzero(img[:,x]==255)
            if num>self.THVMAX:
                if np.count_nonzero(xOld==255)>num:
                    img[:,x]=xOld
                lock=True
            if num<=self.THVMAX and num>=self.THVMIN and lock:
                img[:,x]=xOld
            if num<=self.THVMAX and num>=self.THVMIN and not lock:
                img[:,x]=0
                lock=True
            xOld=img[:,x]
        lock=False
        for y in range(self.img_data["图片高度"]):
            num=np.count_nonzero(img[y,:]==255)
            if num>self.THVMAX:
                if np.count_nonzero(yOld==255)>num and np.count_nonzero(yOld==255)-num>3:
                    img[y,:]=yOld
                lock=True
            if num<=self.THVMAX and num>=self.THVMIN and lock:
                img[y,:]=yOld
            if num<=self.THVMAX and num>=self.THVMIN and not lock:
                img[y,:]=0
                lock=True
            yOld=img[y,:]
            #cv2.imshow('image',img)
            #cv2.waitKey(0)
        lock=False
        for x in range(self.img_data["图片宽度"]-1,0,-1):
            num=np.count_nonzero(img[:,x]==255)
            if num>self.THVMAX:
                if np.count_nonzero(xOld==255)>num:
                    img[:,x]=xOld
                lock=True
            if num<=self.THVMAX and num>=self.THVMIN and lock:
                img[:,x]=xOld
            if num<=self.THVMAX and num>=self.THVMIN and not lock:
                img[:,x]=0
                lock=True
            xOld=img[:,x]
        lock=False
        for y in range(self.img_data["图片高度"]-1,0,-1):
            num=np.count_nonzero(img[y,:]==255)
            if num>self.THVMAX:
                if np.count_nonzero(yOld==255)>num and np.count_nonzero(yOld==255)-num>3:
                    img[y,:]=yOld
                lock=True
            if num<=self.THVMAX and num>=self.THVMIN and lock:
                img[y,:]=yOld
            if num<=self.THVMAX and num>=self.THVMIN and not lock:
                img[y,:]=0
                lock=True
            yOld=img[y,:]
        return img
if __name__ == '__main__':
    img = cv2.imread('res/image/photos.bmp',cv2.IMREAD_GRAYSCALE)
    numax=np.max(img)
    numin=np.min(img)
    yI,xI=np.shape(img)
    Image_pro=imageProFast(img,numin,numax,yI,xI)
    img=Image_pro.imageRap()
    cv2.imshow('image',img)
    cv2.waitKey(0)