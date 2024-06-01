from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QObject,Signal,Slot,QProcess,QTimer,Qt,QByteArray,QBuffer,QIODevice
from PySide6.QtWidgets import QApplication
from PySide6.QtQuick import QQuickView
from PySide6.QtGui import QGuiApplication,QImage
import cv2
import numpy as np
import sys
from NBri import*
import base64  
import json
functionCCPath=sys.argv[1]
with open(functionCCPath,'r') as f:
    functionCC = f.read()
    if functionCC is not None:
        fV=json.loads(functionCC)
decodedBytes=base64.b64decode(fV[-1])#上面是将base64编码的图像数据从QByteArray通过base64解码读取转换为Bytes
nparr=np.frombuffer(decodedBytes,np.uint8)  
Img=cv2.imdecode(nparr,cv2.IMREAD_GRAYSCALE)#传输的图像
Img=cv2.imread('res/image/input/2.bmp',cv2.IMREAD_GRAYSCALE)
numax=np.max(Img)
numin=np.min(Img)
yI,xI=np.shape(Img)
Image_pro=imageProFast(Img,numin,numax,yI,xI,fV[1],fV[2],fV[3],-0.3,1)
Img=Image_pro.imageRap()
Img=cv2.getRectSubPix(Img,(yI,yI),(xI//2,yI//2))
PImage=QImage(Img.data, Img.shape[1], Img.shape[0], Img.strides[0], QImage.Format_Grayscale8)#QImage.Format_RGB888为彩色转码格式
byte_array=QByteArray()
buffer=QBuffer(byte_array)
buffer.open(QIODevice.WriteOnly)
PImage.save(buffer, "PNG")
# 将 QByteArray 转换为 base64 编码的字符串
ImgBase64=byte_array.toBase64().data().decode()
print(ImgBase64)
sys.stdout.flush()