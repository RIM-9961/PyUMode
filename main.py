#———————————————————————————————————————#                          
#      ______     __     __    __       #
#     /\  == \   /\ \   /\ "-./  \      #
#     \ \  __<   \ \ \  \ \ \-./\ \     #
#      \ \_\ \_\  \ \_\  \ \_\ \ \_\    #
#       \/_/ /_/   \/_/   \/_/  \/_/    #
#                                       #                          
#———————————————————————————————————————#   
#作者的github主页https://github.com/RIM-9961?tab=repositories                       
#mayavi部分摘自官网文档http://docs.enthought.com/mayavi/mayavi/auto/example_qt_embedding.html#example-qt-embedding
#ps.大部分注释由GEEX生成，我是真懒得写注释了
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QObject,Signal,Slot,QProcess,QTimer,Qt,QByteArray,QBuffer,QIODevice
from PySide6.QtWidgets import QApplication
from PySide6.QtQuick import QQuickView
from PySide6.QtGui import QGuiApplication,QImage
from __init__ import*
#要是import*能自动识别该多好 
class PumdWork(QObject):#定义一个类，继承自QObject广设比赛UI控制面板
    imageData=Signal(str)
    imageDataIn=Signal(str)
    def __init__(self):
        super().__init__()
        self.Img=None
    def uiUpdate(self,name,spacename):#更新UI
        for rootObject in engine.rootObjects():
            if rootObject.title()==name:
                rootObject.close()
        engine.load("qrc:qml/qml/"+spacename+".qml")
        for rootObject in engine.rootObjects():
            if rootObject.title()==name:
                rootObject.setFlags(rootObject.flags() | Qt.WindowStaysOnTopHint)
    @Slot()
    def About(self):#打开关于界面
        self.uiUpdate("团队介绍","GRAbout")
    @Slot()
    def CameraControl(self):#打开相机控制
        self.uiUpdate("相机控制","CameraControl")
    @Slot()
    def functionControl(self):#打开功能控制
        self.uiUpdate("参数调整","FuncValControl")
    @Slot()
    def start(self):#开始按钮
        self.inputImg()
        print("开始")
    @Slot()
    def outputImg(self):#输出图像按钮
        if self.Img is None:
            print("未检测到图像")
        else:
            cv2.imwrite("res/image/output/"+str(time.time())+".bmp",self.Img)
            print("输出图像")
    def inputImg(self):
        Img=cv2.imread('res/image/input/2.bmp',cv2.IMREAD_GRAYSCALE)
        numax=np.max(Img)
        numin=np.min(Img)
        yI,xI=np.shape(Img)
        Image_pro=imageProFast(Img,numin,numax,yI,xI)
        Img=Image_pro.imageRap()
        Img=cv2.getRectSubPix(Img,(yI,yI),(xI//2,yI//2))
        self.Img=Img
        PImage=QImage(Img.data, Img.shape[1], Img.shape[0], Img.strides[0], QImage.Format_Grayscale8)#QImage.Format_RGB888为彩色转码格式
        byte_array=QByteArray()
        buffer=QBuffer(byte_array)
        buffer.open(QIODevice.WriteOnly)
        PImage.save(buffer, "PNG")
        # 将 QByteArray 转换为 base64 编码的字符串
        ImgBase64=byte_array.toBase64().data().decode()
        self.imageData.emit(ImgBase64)
def findCameraListen(process):
    data = process.readAllStandardOutput().data().decode()
    print("Received from child process:", data)
def main(loadProcess):#注册引擎加载界面
    loadProcess.terminate()
    global engine
    app=QApplication()
    engine=QQmlApplicationEngine()
    PW=PumdWork()
    FluentUI.init(engine)
    rootContext=engine.rootContext()
    rootContext.setContextProperty("DetectControl",PW)
    engine.load("qrc:qml/qml/GRMainScreen.qml")
    findCamera=QProcess()
    findCamera.start(sys.executable,["res/function/camera_send.py"])
    findCamera.readyReadStandardOutput.connect(findCameraListen(findCamera))
    atexit.register(OffAll,[loadProcess,findCamera])
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
    args[0].terminate()
    print("关闭")
if __name__  == '__main__':
    loadProcess=Process(name='loadProcess',target=load)
    loadProcess.start()
    main(loadProcess)
