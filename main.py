#———————————————————————————————————————#                          
#      ______     __     __    __       #
#     /\  == \   /\ \   /\ "-./  \      #
#     \ \  __<   \ \ \  \ \ \-./\ \     #
#      \ \_\ \_\  \ \_\  \ \_\ \ \_\    #
#       \/_/ /_/   \/_/   \/_/  \/_/    #
#                                       #                          
#———————————————————————————————————————#   
#作者的github主页https://github.com/RIM-9961?tab=repositories                       
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QObject,Signal,Slot,QProcess,QTimer,Qt,QByteArray,QBuffer,QIODevice
from PySide6.QtWidgets import QApplication
from PySide6.QtQuick import QQuickView
from PySide6.QtGui import QGuiApplication,QImage
from __init__ import*
import tempfile
import json
import base64  
import ast
with tempfile.NamedTemporaryFile(delete=False) as cameraCCPath:
    cameraCCPath = cameraCCPath.name
class PumdWork(QObject):#定义一个类，继承自QObject广设比赛UI控制面板
    imageData=Signal(str)
    imageDataIn=Signal(str)
    getCameraCC=Signal()
    baoGuangTime=Signal(int)
    def __init__(self):
        super().__init__()
        self.Img=None
        self.cameraCC=None
        self.ImgData=None
        self.isFirst=True
    def uiUpdate(self,name,spacename):#更新UI
        for rootObject in engine.rootObjects():
            if rootObject.title()==name:
                rootObject.close()
        engine.load("qrc:qml/qml/"+spacename+".qml")
        for rootObject in engine.rootObjects():
            if rootObject.title()==name:
                rootObject.setFlags(rootObject.flags() | Qt.WindowStaysOnTopHint)
    def cleanNeiCun(self):#清空相机控制等子进程在没被调用情况下的内存
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
        with open(cameraCCPath, 'w') as f:
            ccList = json.dumps(ccList)
            f.write(ccList)
    @Slot()
    def About(self):#打开关于界面
        self.uiUpdate("团队介绍","GRAbout")
    @Slot()
    def CameraControl(self):#打开相机控制
        if self.cameraCC is not None:self.cameraCC.close()
        self.cameraCC=QProcess()
        self.cameraCC.start("python",["res/function/camera_control.py",engine])#生成一个检测相机控制窗口并返回调整值的进程
        self.cameraCC.readyReadStandardOutput.connect(self.cleanNeiCun)
        self.uiUpdate("相机控制","CameraControl")
        if self.ImgData ==None and self.isFirst == True:
            QTimer.singleShot(500,self.CameraControl)
        if self.ImgData !=None and self.isFirst == True:
            self.isFirst=False
            with open(cameraCCPath, 'w') as f:
                ccList = json.dumps(self.ccList.append(self.isFirst))
                f.write(ccList)
            self.CameraControl()
        if self.ImgData !=None and self.isFirst == False:
            self.baoGuangTime.emit(round(self.ImgData[0][1]))#发送相机初始值重新更新UI
    @Slot()
    def functionControl(self):#打开功能控制
        self.uiUpdate("参数调整","FuncValControl")
    @Slot()
    def start(self):#开始按钮
        self.inputImg=QProcess()
        self.inputImg.start("python",["res/function/image_input.py","这里写传入的Img路径"])
        self.inputImg.readyReadStandardOutput.connect(self.inputImg2Qml)
        print("开始")
    @Slot()
    def outputImg(self):#输出图像按钮
        if self.Img is None:
            print("未检测到图像")
        else:
            cv2.imwrite("res/image/output/"+str(time.time())+".bmp",self.Img)
            print("输出图像")
    def inputImg2Qml(self):
        ImgBase64 = self.inputImg.readAllStandardOutput()
        ImgBase64 == bytes(ImgBase64).decode("gbk")
        self.imageData.emit(ImgBase64.data().decode())
        decoded_bytes = base64.b64decode(ImgBase64)  
        nparr = np.frombuffer(decoded_bytes, np.uint8)  
        self.Img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
    def findCameraListen(self):
        if self.findCamera is None:
            return
        Img = self.findCamera.readAllStandardOutput()
        Img = bytes(Img).decode("gbk")
        if "isImgData" in Img:
            self.ImgData=ast.literal_eval(Img[Img.find("isImgData")+9:][:Img[Img.find("isImgData")+9:].find("]")+1])#输出原图像属性
        else:
            self.imageDataIn.emit(Img)
    def findCameraSend(self):
        self.findCamera=QProcess()
        self.findCamera.start("python",["res/function/camera_send.py",cameraCCPath])
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
if __name__  == '__main__':
    loadProcess=Process(name='loadProcess',target=load)
    loadProcess.start()
    main(loadProcess)
