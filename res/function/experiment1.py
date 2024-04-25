from time import*
import cv2
import numpy as np
img=cv2.imread("res\image\ppp.png")
img=cv2.cvtColor(img,cv2.COLOR_RGB2GRAY) if img.shape[2]==3 else img
img=cv2.resize(img,(1000,1000))
_,img=cv2.threshold(img,50,255,cv2.THRESH_BINARY)
F_EXAMPLE = cv2.FastFeatureDetector.create()
points = F_EXAMPLE.detect(img, None)
img_n=img.copy().astype(np.uint8)
for i in range(-90,90):
    angle = i  # 旋转角度
    center = (1000, 1000)  # 旋转中心
    scale = 1.0  # 缩放因子
    anchor = cv2.getRotationMatrix2D(center, angle, scale)
    img_r = cv2.warpAffine(img, anchor, (1000, 1000))
    img_=np.zeros_like(img)
    img_=np.where(img_n==0,-255,img_n)+img_
    img_n=img_r+img_
    img_n=np.where(img_n<0,0,img_n)
    img_n=np.where(img_n>=1000,25500,img_n)
    cv2.imshow("img_n",img_n)
    cv2.waitKey(1)
img_n=(img_n/100).astype(np.uint8)
img_n_=np.zeros_like(img_n)
img_n__=np.zeros_like(img_n)
contours, hierarchy = cv2.findContours(img_n, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)                 #获取杂点图的轮廓
for contour in contours:
    area = cv2.contourArea(contour)
    point_list=[]
    if area < 100:                                                                                  #根据面积阈值判断是否为杂点
        cv2.drawContours(img_n_, contour, -1, (255, 0, 0), 2)                                       #绘制小轮廓于img_n_
k = np.ones((5,5), np.uint8)                                                                        #对图像进行膨胀操作
img_n_ = cv2.dilate(img_n_, k, iterations=1)
contours_, hierarchy_ = cv2.findContours(img_n_, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)              #获取膨胀后的轮廓
for contour_ in contours_:
    point_list=[]
    for point in points:
        if point in contour_:
            point_list.append(point)
            if len(point_list)>=2:
                cv2.line(img_n__,tuple(point_list[0]),tuple(point_list[1]),(255,0,0),2)
cv2.imshow("img_n__",img_n_)
cv2.waitKey(0)
