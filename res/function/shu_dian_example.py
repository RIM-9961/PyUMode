import cv2
import time
import numpy as np
import matplotlib.pyplot as plt
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
        self.imgRy=range(yI)
        self.imgRy_=range(yI-1,0,-1)
        self.imgRx=range(xI)
        self.imgRx_=range(xI-1,0,-1)
    def imageRap(self)->cv2.typing.MatLike:#这是图像require和process操作
        imgdata=self.img_data
        edged = cv2.Canny(imgdata["图片矩阵"], 50, 150)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (13, 13))
        closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
        edged = cv2.Canny(closed, 50, 150)
        contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            peri = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
            if len(approx) == 4:
                pts1 = np.float32([point[0] for point in approx])
                side_length = 1000
                pts2 = np.float32([[0, 0], [side_length, 0], [side_length, side_length], [0, side_length]])
                M = cv2.getPerspectiveTransform(pts1, pts2)
                imgdata["图片矩阵"] = cv2.warpPerspective(imgdata["图片矩阵"], M, (side_length, side_length))
        imgdata["图片矩阵"]=cv2.flip(imgdata["图片矩阵"],1)
        h,w=np.shape(imgdata["图片矩阵"])
        cv2.imshow("img",imgdata["图片矩阵"][0:10,:])
        cv2.waitKey(0)
        a=input("请输入上张图片像素点阈值：")
        cv2.imshow("img",imgdata["图片矩阵"][h-10:h,:])
        cv2.waitKey(0)
        b=input("请输入上张图片像素点阈值：")
        cv2.imshow("img",imgdata["图片矩阵"][:,0:10])
        cv2.waitKey(0)
        c=input("请输入上张图片像素点阈值：")
        cv2.imshow("img",imgdata["图片矩阵"][:,w-10:w])
        cv2.waitKey(0)
        d=input("请输入上张图片像素点阈值：")
        for i in range(w):
            if np.count_nonzero(imgdata["图片矩阵"][0:10,i]>=200)<=int(a):
                imgdata["图片矩阵"][0:10,i]=0
            else:
                imgdata["图片矩阵"][0:10,i]=255
        for i in range(w):
            if np.count_nonzero(imgdata["图片矩阵"][h-10:h,i]>=200)<int(b):
                imgdata["图片矩阵"][h-10:h,i]=0
            else:
                imgdata["图片矩阵"][h-10:h,i]=255
        for i in range(h):
            if np.count_nonzero(imgdata["图片矩阵"][i,0:10]>=200)<=int(c):
                imgdata["图片矩阵"][i,0:10]=0
            else:
                imgdata["图片矩阵"][i,0:10]=255
        for i in range(h):
            if np.count_nonzero(imgdata["图片矩阵"][i,w-10:w]>=200)<=int(d):
                imgdata["图片矩阵"][i,w-10:w]=0
            else:
                imgdata["图片矩阵"][i,w-10:w]=255
        _,self.img_data["图片矩阵"]=cv2.threshold(imgdata["图片矩阵"],imgdata["最大灰度值"]//self.BLI,imgdata["最大灰度值"],cv2.THRESH_OTSU)
        img=self.countPixel([1,h-2,1,w-2])
        return img
    def writeText(self,img,text,position)->cv2.typing.MatLike:#写文字
        font=cv2.FONT_HERSHEY_SIMPLEX
        color=(255,255,255)#白色
        cv2.putText(img,text,position,font,self.font_size,color,2,cv2.LINE_AA)
        cv2.waitKey(0)
        return img
    def countPixel(self,pointList)->cv2.typing.MatLike:#统计缺口像素点(没装装饰器的原因是懒)
        value=0
        v1=[]
        v2=[]
        v3=[]
        v4=[]
        h1,h2,w1,w2=pointList
        img=self.img_data["图片矩阵"]
        for point in range(w1,w2):
            j=img[h1,point]
            if j==255:
                img[h1,point]=0
                if point<2*(w2-w1)/3 and len(v1)==0 and point>(w2-w1)/3:
                    self.writeText(img,str(0),[int((w2-w1)/3-50),h1+40])
                    v1.append(0)
                if point<w2-w1 and len(v1)==1 and point>2*(w2-w1)/3:
                    self.writeText(img,str(0),[int(2*(w2-w1)/3-50),h1+40])
                    v1.append(0)
                if point==w2-w1-1 and len(v1)==2:
                    self.writeText(img,str(0),[int((w2-w1)-50),h1+40])
                    v1.append(0)
                if value!=0:
                    value=round(value*((abs(w1-w2)+2)/1000))
                    img=self.writeText(img,str(value),[point,h1+40])
                    v1.append(value)
                value=0
            elif j==0:value+=1
        for point in range(w1,w2):
            j=img[h2,point]
            if j==255:
                img[h2,point]=0
                if point<2*(w2-w1)/3 and len(v2)==0 and point>(w2-w1)/3:
                    self.writeText(img,str(0),[int((w2-w1)/3-50),h1+40])
                    v2.append(0)
                if point<w2-w1 and len(v2)==1 and point>2*(w2-w1)/3:
                    self.writeText(img,str(0),[int(2*(w2-w1)/3-50),h1+40])
                    v2.append(0)
                if point==w2-w1-1 and len(v2)==2:
                    self.writeText(img,str(0),[int((w2-w1)-50),h1+40])
                    v2.append(0)
                if value!=0:
                    value=round(value*((abs(w1-w2)+2)/1000))
                    img=self.writeText(img,str(value),[point,h2-20])
                    v2.append(value)
                value=0
            elif j==0:value+=1
        for point in range(h1,h2):
            j=img[point,w1]
            if j==255:
                img[point,w1]=0
                if point<2*(h2-h1)/3 and len(v3)==0 and point>(h2-h1)/3:
                    self.writeText(img,str(0),[w1+20,int((h2-h1)/3-50)])
                    v3.append(0)
                if point<h2-h1 and len(v3)==1 and point>2*(h2-h1)/3:
                    self.writeText(img,str(0),[w1+20,int(2*(h2-h1)/3-50)])
                    v3.append(0)
                if point==h2-h1-1 and len(v3)==2:
                    self.writeText(img,str(0),[w1+20,int((h2-h1)-50)])
                    v3.append(0)
                if value!=0:
                    value=round(value*((abs(h1-h2)+2)/1000))
                    img=self.writeText(img,str(value),[w1+20,point])
                    v3.append(value)
                value=0
            elif j==0:value+=1
        for point in range(h1,h2):
            j=img[point,w2]
            if j==255:
                img[point,w2]=0
                if point<2*(h2-h1)/3 and len(v4)==0 and point>(h2-h1)/3:
                    self.writeText(img,str(0),[w2-50,int((h2-h1)/3-50)])
                    v4.append(0)
                if point<h2-h1 and len(v4)==1 and point>2*(h2-h1)/3:
                    self.writeText(img,str(0),[w2-50,int(2*(h2-h1)/3-50)])
                    v4.append(0)
                if point==h2-h1-1 and len(v4)==2:
                    self.writeText(img,str(0),[w2-50,int((h2-h1)-50)])
                if value!=0:
                    value=round(value*((abs(h1-h2)+2)/1000))
                    img=self.writeText(img,str(value),[w2-50,point])
                    v4.append(value)
                value=0
            elif j==0:value+=1
        return img
if __name__ == '__main__':
    img=cv2.imread('res/image/output/13.bmp',cv2.IMREAD_GRAYSCALE)
    numax=np.max(img)
    numin=np.min(img)
    yI,xI=np.shape(img)
    Image_pro=imageProFast(img,numin,numax,yI,xI,600,20,1,0,1)
    img=Image_pro.imageRap()
    cv2.imshow("img",img)
    cv2.waitKey(0)