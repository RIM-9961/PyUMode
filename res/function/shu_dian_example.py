import cv2
import time
import numpy as np
#@RIM(这个人写的)->https://github.com/RIM-9961
#让幼儿园大班都能看懂程度的能力
#保姆级代码
class imageProFast:#快速图像处理类
    def __init__(self,img,numin,numax,yI,xI,THVMAX,THVMIN,BLI,angle,font_size):#这是注册信息
        self.img_data={"图片矩阵":img,"最小灰度值":numin,"最大灰度值":numax,"图片高度":yI,"图片宽度":xI}#图像信息字典
        self.THVMAX=THVMAX#900#这是过滤比例(高)
        self.THVMIN=THVMIN#10#这是过滤比例(低)
        self.BLI=BLI#2.5#这是图像二值化比例
        self.angle=angle#-0.3#图像旋转角度
        self.font_size=font_size#1#这是标记字体时字体大小
        #以下为定值,不用改
        self.imgRy=range(yI)
        self.imgRy_=range(yI-1,0,-1)
        self.imgRx=range(xI)
        self.imgRx_=range(xI-1,0,-1)
    def imageRap(self)->cv2.typing.MatLike:#这是图像require和process操作
        imgdata=self.img_data
        _,img=cv2.threshold(imgdata["图片矩阵"],imgdata["最大灰度值"]//self.BLI,imgdata["最大灰度值"],cv2.THRESH_OTSU)
        img=self.rotateImage(img,self.angle)#旋转图像操作
        _,img=cv2.threshold(img,imgdata["最大灰度值"]//self.BLI,imgdata["最大灰度值"],cv2.THRESH_OTSU)
        img=self.cleanCenter(img)#中心标签去除操作
        img=self.cleanEdge(img)#边缘杂边去除操作(第一遍)
        img=self.cleanEdge(img)#边缘杂边去除操作(第二遍消除边缘误差)
        img=self.cleanPoints(img)#杂点去除操作
        img=self.countPixel(img)#输出缺口像素点图像
        np.save("res/npy/img.npy",img)
        return img
    def rotateImage(self,img,angle)->cv2.typing.MatLike:#通过warpAffine旋转(老朋友了)
        yI,xI=self.img_data["图片高度"],self.img_data["图片宽度"]
        center=(xI//2, yI//2) #旋转中心
        scale=1.0 #缩放因子
        anchor=cv2.getRotationMatrix2D(center, angle, scale)
        img=cv2.warpAffine(img, anchor, (xI, yI))
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
    def cleanEdge(self,img)-> cv2.typing.MatLike:#通过遍历横纵坐标完善图像，使边缘更整齐(写罗嗦了)
        lock=False
        for x in self.imgRx:
            num=np.count_nonzero(img[:,x]==255)
            if num>self.THVMAX:
                if np.count_nonzero(xOld==255)>num and np.count_nonzero(xOld==255)-num>3:
                    img[:,x]=xOld
                if np.count_nonzero(xOld==255)<num and num-np.count_nonzero(xOld==255)<=3:
                    img[:,x]=xOld
                lock=True
            if num<=self.THVMAX and num>=self.THVMIN and lock:img[:,x]=xOld
            if num<=self.THVMAX and num>=self.THVMIN and not lock:
                img[:,x]=0
                lock=True
            xOld=img[:,x]
        lock=False
        cv2.imshow("img",img)
        cv2.waitKey(0)
        for y in self.imgRy:
            num=np.count_nonzero(img[y,:]==255)
            if num>self.THVMAX:
                if np.count_nonzero(yOld==255)>num and np.count_nonzero(yOld==255)-num>3:
                    img[y,:]=yOld
                if np.count_nonzero(yOld==255)<num and num-np.count_nonzero(yOld==255)<=3:
                    img[y,:]=yOld
                lock=True
            if num<=self.THVMAX and num>=self.THVMIN and lock:img[y,:]=yOld
            if num<=self.THVMAX and num>=self.THVMIN and not lock:
                img[y,:]=0
                lock=True
            yOld=img[y,:]
        lock=False
        for x in self.imgRx_:
            num=np.count_nonzero(img[:,x]==255)
            if num>self.THVMAX:
                if np.count_nonzero(xOld==255)>num and np.count_nonzero(xOld==255)-num>3:
                    img[:,x]=xOld
                if np.count_nonzero(xOld==255)<num and num-np.count_nonzero(xOld==255)<=3:
                    img[:,x]=xOld
                lock=True
            if num<=self.THVMAX and num>=self.THVMIN and lock:img[:,x]=xOld
            if num<=self.THVMAX and num>=self.THVMIN and not lock:
                img[:,x]=0
                lock=True
            xOld=img[:,x]
        lock=False
        for y in self.imgRy_:
            num=np.count_nonzero(img[y,:]==255)
            if num>self.THVMAX:
                if np.count_nonzero(yOld==255)>num and np.count_nonzero(yOld==255)-num>3:
                    img[y,:]=yOld
                if np.count_nonzero(yOld==255)<num and num-np.count_nonzero(yOld==255)<=3:
                    img[y,:]=yOld
                lock=True
            if num<=self.THVMAX and num>=self.THVMIN and lock:img[y,:]=yOld
            if num<=self.THVMAX and num>=self.THVMIN and not lock:
                img[y,:]=0
                lock=True
            yOld=img[y,:]
        return img
    def cleanPoints(self,img)-> cv2.typing.MatLike:#清除杂点
        contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            area = cv2.contourArea(contour)
            if area < 5:
                cv2.drawContours(img, [contour], 0, 0, -1)
        return img
    def writeText(self,img,text,position)->cv2.typing.MatLike:#写文字
        font=cv2.FONT_HERSHEY_SIMPLEX
        color=(255,255,255)#白色
        cv2.putText(img,text,position,font,self.font_size,color,2,cv2.LINE_AA)
        return img
    def countPixel(self,img)->cv2.typing.MatLike:#统计缺口像素点(没装装饰器的原因是懒)
        fP={}#创建"L1","L2","R1","R2"的储存字典
        LR1List=[]
        LR2List=[]
        LLList=[]
        RRList=[]
        value=0
        for y in self.imgRy:
            for x in self.imgRx:
                if img[y,x]==255:
                    fP["L2"]=[y,x]
                    break
        for y in self.imgRy_:
            for x in self.imgRx:
                if img[y,x]==255:
                    fP["L1"]=[y,x]
                    break
        for y in self.imgRy:
            for x in self.imgRx_:
                if img[y,x]==255:
                    fP["R2"]=[y,x]
                    break
        for y in self.imgRy_:
            for x in self.imgRx_:
                if img[y,x]==255:
                    fP["R1"]=[y,x]
                    break
        for i in range(fP["L1"][0],fP["L2"][0]):
            j=img[i,fP["L1"][1]]
            if j==255:
                if value!=0:
                    value=round(value*(abs(fP["L1"][0]-fP["L2"][0])/1000))
                    LLList.append(value)
                    img=self.writeText(img,str(value),[fP["L1"][1]+10,i])
                value=0
            elif j==0:value+=1
        for i in range(fP["R1"][0],fP["R2"][0]):
            j=img[i,fP["R1"][1]]
            if j==255:
                if value!=0:
                    value=round(value*(abs(fP["R1"][0]-fP["R2"][0])/1000))
                    RRList.append(value)
                    img=self.writeText(img,str(value),[fP["R1"][1]-40,i])
                value=0
            elif j==0:value+=1
        for i in range(fP["L2"][1],fP["R2"][1]):
            j=img[fP["L2"][0],i]
            if j==255:
                if value!=0:
                    value=round(value*(abs(fP["L2"][1]-fP["R2"][1])/1000))
                    LR2List.append(value)
                    img=self.writeText(img,str(value),[i,fP["L2"][0]-10])
                value=0
            elif j==0:value+=1
        for i in range(fP["L1"][1],fP["R1"][1]):
            j=img[fP["L1"][0],i]
            if j==255:
                if value!=0:
                    value=round(value*(abs(fP["L1"][1]-fP["R1"][1])/1000))
                    LR1List.append(value)
                    img=self.writeText(img,str(value),[i,fP["L1"][0]+40])
                value=0
            elif j==0:value+=1
        return img
if __name__ == '__main__':
    img=cv2.imread('res/image/output/13.bmp',cv2.IMREAD_GRAYSCALE)
    numax=np.max(img)
    numin=np.min(img)
    yI,xI=np.shape(img)
    Image_pro=imageProFast(img,numin,numax,yI,xI,600,20,1,-0.2,1)
    img=Image_pro.imageRap()
    cv2.imshow("img",img)
    cv2.waitKey(0)