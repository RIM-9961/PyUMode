#———————————————————————————————————————#                          
#      ______     __     __    __       #
#     /\  == \   /\ \   /\ "-./  \      #
#     \ \  __<   \ \ \  \ \ \-./\ \     #
#      \ \_\ \_\  \ \_\  \ \_\ \ \_\    #
#       \/_/ /_/   \/_/   \/_/  \/_/    #
#                                       #                          
#———————————————————————————————————————#   
#作者的github主页https://github.com/RIM-9961?tab=repositories 
# 并没有写热更新，刚开始的时候没想到有这么多                      
from PySide6.QtQml import QQmlApplicationEngine,QQmlFileSelector,QQmlContext
from PySide6.QtCore import QObject,Signal,Slot,QProcess,QTimer,Qt,QByteArray,QBuffer,QIODevice
from PySide6.QtWidgets import QApplication
from PySide6.QtQuick import QQuickView,QQuickWindow,QQuickItem
from PySide6.QtGui import QGuiApplication,QImage
from multiprocessing import Process, Queue
import tempfile
import json
import base64  
import numpy as np
import cv2
import ast
import time
import os
import sys
import atexit
import FluentUI
from res.resdata_rc import *
with tempfile.NamedTemporaryFile(delete=False) as cameraCCPath:
    cameraCCPath=cameraCCPath.name
with tempfile.NamedTemporaryFile(delete=False) as functionCCPath:
    functionCCPath=functionCCPath.name
with tempfile.NamedTemporaryFile(delete=False) as imgPath:
    imgPath=imgPath.name
absPath = os.path.dirname(os.path.abspath(__file__))
ruleFilePath = os.path.join(absPath,"res")
python_interpreter = os.path.join(absPath,"python")+"\python.exe" if getattr(sys, 'frozen', False) else sys.executable
class PumdWork(QObject):#定义一个类，继承自QObject广设比赛UI控制面板
    imageData=Signal(str)
    imageDataIn=Signal(str)
    getCameraCC=Signal()
    openCameraCC=Signal()
    closeCameraCC=Signal()
    baoGuangTime=Signal(int)
    def __init__(self):
        super().__init__()
        self.Img=None
        self.ImgN=None
        self.cameraCC=None
        self.ImgData=None
        self.isFirst=True
        self.functionVList=['默认', 900.0, 10.0, 2.5, 0.0, 0.0, 0.0]#功能控制参数
        self.functionVListOld=None#功能控制上一次的参数（可退回）
    def uiUpdate(self,name,spacename):#更新UI
        for rootObject in engine.rootObjects():
            if rootObject.title()==name:
                rootObject.close()
        engine.load("qrc:qml/qml/"+spacename+".qml")
        for rootObject in engine.rootObjects():
            if rootObject.title()==name:
                rootObject.setFlags(rootObject.flags() | Qt.WindowStaysOnTopHint)
    def CleanNeiCun(self):#清空相机控制等子进程在没被调用情况下的内存
        self.getCameraCC.emit()
        lock=True
        for rootObject in engine.rootObjects():
            if rootObject.title()=="相机控制":
                lock=False
        if lock:self.cameraCC.close()
    @Slot(list)
    def GetCameraCC(self,ccList):#获取相机控制进程
        self.ccList=ccList
        lock=True
        for rootObject in engine.rootObjects():
            if rootObject.title()=="相机控制":
                lock=False
        if lock:self.cameraCC.close()
        ccList.append(self.isFirst)
        with open(cameraCCPath,'w') as f:
            ccList=json.dumps(ccList)
            f.write(ccList)
    @Slot()
    def About(self):#打开关于界面
        self.uiUpdate("团队介绍","GRAbout")
    @Slot()
    def CameraControl(self):#打开相机控制界面，并运行相机控制进程
        if self.cameraCC is not None:self.cameraCC.close()
        self.cameraCC=QProcess()
        self.cameraCC.start(python_interpreter,[ruleFilePath+"/function/camera_control.py",engine])#生成一个检测相机控制窗口并返回调整值的进程
        self.cameraCC.readyReadStandardOutput.connect(self.CleanNeiCun)
        self.uiUpdate("相机控制","CameraControl")
        if self.ImgData ==None and self.isFirst==True:
            QTimer.singleShot(500,self.CameraControl)
        if self.ImgData !=None and self.isFirst==True:
            self.isFirst=False
            with open(cameraCCPath,'w') as f:
                ccList=json.dumps(self.ccList.append(self.isFirst))
                f.write(ccList)
            self.CameraControl()
        if self.ImgData !=None and self.isFirst==False:
            self.baoGuangTime.emit(round(self.ImgData[0][1]))#发送相机初始值重新更新UI
    @Slot()
    def functionControl(self):#只是打开功能控制界面
        self.functionVListOld=self.functionVList
        self.uiUpdate("参数调整","FuncValControl")
    @Slot()
    def start(self):#开始按钮
        if self.Img !=None:
            #--------------------------------------------------------------------------------------处理过程
            with open(imgPath,'w') as f:
                imgList=json.dumps([self.Img])#这里写上参数调整值
                f.write(imgList)
            self.imgProgress=QProcess()
            self.imgProgress.start(python_interpreter,[ruleFilePath+"/function/image_progress.py",imgPath])
            self.imgProgress.readyReadStandardOutput.connect(self.imageProgress)
            #--------------------------------------------------------------------------------------处理过程
    @Slot()
    def outputImg(self):#输出图像按钮
        if self.ImgN is None:
            print("未检测到图像")
        else:
            cv2.imwrite(ruleFilePath+"/image/output/"+str(time.time())+".bmp",self.ImgN)
            print("输出图像")
    @Slot(list,result=list)
    def GetFunctionCC(self,ccList):#获取功能控制参数
        if ccList!=[] and self.functionVList is None:
            self.functionVList=ccList
            self.functionVListOld=ccList
        elif ccList!=[] and ccList!=self.functionVListOld:
            self.functionVList=ccList
        else:
            return self.functionVList
        print(self.functionVList)
    def imageProgress(self):#图像处理
        img=self.imgProgress.readAllStandardOutput()
        img=bytes(img).decode("gbk")
        functionVList=self.functionVList
        functionVList.append(img)
        with open(functionCCPath,'w') as f:
            functionVList=json.dumps(functionVList)#这里写上参数调整值
            f.write(functionVList)
        self.inputImg=QProcess()
        self.inputImg.start(python_interpreter,[ruleFilePath+"/function/image_input.py",functionCCPath])
        self.inputImg.readyReadStandardOutput.connect(self.inputImg2Qml)
        print("开始")
    def errorI(self):#图像处理出错
        print("图像处理出错")
    def inputImg2Qml(self):#图像处理向右侧显示窗口传递图片信息
        img=self.inputImg.readAllStandardOutput()
        img=bytes(img).decode("gbk")
        self.imageData.emit(img)#向右侧显示窗口传递图片信息
    def findCameraListen(self):#监听子进程相机输出
        if self.findCamera is None:
            print("相机控制进程未开启")
            return
        Img=self.findCamera.readAllStandardOutput()
        Img=bytes(Img).decode("gbk")
        if "isImgData" in Img:
            self.ImgData=ast.literal_eval(Img[Img.find("isImgData")+9:][:Img[Img.find("isImgData")+9:].find("]")+1])#输出原图像属性
            if self.ImgData[0][1]==0.0:
                print("未检测到图像")
                self.closeCameraCC.emit()
        else:
            self.Img=Img
            self.openCameraCC.emit()
            self.imageDataIn.emit(Img)
    def findCameraSend(self):#运行相机开启脚本进程
        print("相机控制进程开启")
        self.findCamera=QProcess()
        self.findCamera.setProcessChannelMode(QProcess.MergedChannels)
        self.findCamera.start(python_interpreter,[ruleFilePath+"/function/camera_send.py",cameraCCPath])
        self.findCamera.readyReadStandardOutput.connect(self.findCameraListen)
def main(loadProcess):#注册引擎加载界面
    loadProcess.terminate()
    global engine
    global PW
    app=QApplication()
    engine=QQmlApplicationEngine()
    PW=PumdWork()
    FluentUI.init(engine)
    rootContext=engine.rootContext()
    rootContext.setContextProperty("DetectControl",PW)
    engine.load("qrc:qml/qml/GRMainScreen.qml")
    PW.findCameraSend()
    atexit.register(OffAll,loadProcess)
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())
def load():#开机动画
    app=QGuiApplication([])
    view= QQuickView()
    view.setFlags(Qt.ImglessWindowHint)
    view.setSource("qrc:qml/qml/Progress.qml")
    view.show()
    app.exec()
def OffAll(args):#关机函数
    PW.findCamera.close()
    PW.cameraCC.close()
    args.terminate()
    print("关闭")
if __name__ =='__main__':
    loadProcess=Process(name='loadProcess',target=load)
    loadProcess.start()
    main(loadProcess)
