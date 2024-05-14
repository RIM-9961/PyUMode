from time import*
import cv2
import numpy as np
img=cv2.imread("res\image\input\\125.bmp",cv2.IMREAD_GRAYSCALE)
img3=np.zeros_like(img)
x,y=img.shape
k=1
cc=0
'''cK=np.array([[-4,-4,-4],
             [-4-1,2,-1],
             [4,4,4]])
img1=cv2.filter2D(img,-1,cK)'''
cK=np.array([[4,4,4],
             [-1,2,-1],
             [-4,-4,-4]])
img1=cv2.filter2D(img,-1,cK)
img1=cv2.fastNlMeansDenoising(img1, dst=None, h=15,templateWindowSize=10, searchWindowSize=20)
img1=np.where((img1<150)&(img1>50),255,img1)
img1=np.where((img1<=50),0,img1)
contours, _ = cv2.findContours(img1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
areas = [cv2.contourArea(contour) for contour in contours]
min_area = 100
fC = [contour for contour, area in zip(contours, areas) if area >= min_area]
cv2.drawContours(img3, fC, -1, (255, 255, 255),-1)
'''cK=np.array([[-4,-1,4],
             [-4,2,4],
             [-4,-1,4]])
img1=cv2.filter2D(img,-1,cK)'''
cK=np.array([[4,-1,-4],
             [4,2,-4],
             [4,-1,-4]])
img2=cv2.filter2D(img,-1,cK)
img2=cv2.fastNlMeansDenoising(img2, dst=None, h=15,templateWindowSize=10, searchWindowSize=20)
img2=np.where((img2<150)&(img2>20),255,img2)
img2=np.where(img2<=20,0,img2)
contours,_=cv2.findContours(img2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
areas = [cv2.contourArea(contour) for contour in contours]
min_area = 100
fC = [contour for contour, area in zip(contours, areas) if area >= min_area]
cv2.drawContours(img3, fC, -1, (255, 255, 255),-1)
#img2=cv2.divide(np.double(img2),255)**2*255
#img2=np.uint8(img2)
#img=cv2.threshold(img2,100,255,cv2.THRESH_BINARY)[1]
cv2.imshow("img",img3)
cv2.waitKey(0)
cv2.imwrite("res\image\output\\126.bmp",img3)
