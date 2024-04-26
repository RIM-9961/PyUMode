import sys
import cksdk
import time
import cv2
import os
import numpy as np
from ctypes import *
from PySide6.QtCore import QByteArray,QBuffer,QIODevice
from PySide6.QtGui import QImage
import json
import tempfile
while True:
    result=cksdk.CameraEnumerateDevice()
    if result[0]!=0:
        time.sleep(2)
        continue
    result=cksdk.CameraInit(0)#初始化相机
    if result[0]!=0:
        time.sleep(2)
        continue
    hCamera=result[1]
    cksdk.CameraSetIspOutFormat(hCamera, cksdk.CAMERA_MEDIA_TYPE_RGB8)
    cksdk.CameraSetTriggerMode(hCamera, 0)# 设置为连续拍照模式
    cksdk.CameraPlay(hCamera)# 开启相机
    while True:
        cameraCCPath=sys.argv[1]
        try:
            with open(cameraCCPath,'r') as f:
                cameraCC = f.read()
                if cameraCC is not None:
                    cameraCC=json.loads(cameraCC)
                    #cksdk.CameraSetWbMode(hCamera,False)
                    cksdk.CameraSetAeState(hCamera,False)
                    cksdk.CameraSetExposureTime(hCamera,cameraCC[0])
        except:pass
        result=cksdk.CameraGetImageBufferEx(hCamera,1000)
        img_data=result[0]
        if img_data is not None:
            img_info=result[1]
            bytes_count=img_info.iWidth * img_info.iHeight * 3
            img_array=cast(img_data, POINTER(c_char*bytes_count))
            np_arr=np.frombuffer(img_array.contents, dtype=np.uint8, count=bytes_count)
            np_arr.shape=(img_info.iHeight, img_info.iWidth, 3)
            Img=cv2.resize(np_arr, (800, 600))
            PImage=QImage(Img.data, Img.shape[1], Img.shape[0], Img.strides[0], QImage.Format_Grayscale8)#QImage.Format_RGB888为彩色转码格式
            byte_array=QByteArray()
            buffer=QBuffer(byte_array)
            buffer.open(QIODevice.WriteOnly)
            PImage.save(buffer, "PNG")
            ImgBase64=byte_array.toBase64().data().decode()# 将QByteArray 转换为 base64 编码的字符串
            #cv2.imshow("Camera",Img)
            #cv2.waitKey(1)
            print(ImgBase64)
            sys.stdout.flush()
        '''key=cv2.waitKey(30)
        if key == 27 or result[0]==None:
            break
        elif key == ord('b'):
            cksdk.CameraSetOnceWB(hCamera)
    cksdk.CameraPause(hCamera)#暂停相机
    cv2.destroyAllWindows()
    cksdk.CameraUnInit(hCamera)#去初始化相机'''