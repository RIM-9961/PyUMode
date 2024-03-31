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
from PySide6.QtCore import QObject,Signal,Slot,QThread,QTimer,Qt,QByteArray,QBuffer,QIODevice
from PySide6.QtWidgets import QApplication
from PySide6.QtQuick import QQuickView
from PySide6.QtGui import QGuiApplication,QImage
from __init__ import*
#要是import*能自动识别该多好 
class PumdWork(QObject):
    finished = Signal()
    laserData = Signal()
    def __init__(self):
        super().__init__()
    @Slot()
    def About(self):
        engine.load("qrc:qml/qml/GRAbout.qml")
#定义主函数，传入参数loadThread
def main(loadThread):
    loadThread.terminate()
    global engine
    app = QApplication()
    engine = QQmlApplicationEngine()
    PW=PumdWork()
    rootContext = engine.rootContext()
    rootContext.setContextProperty("DetectControl",PW)
    FluentUI.init(engine)
    engine.load("qrc:qml/qml/GRMainScreen.qml")
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())
def load():
    app = QGuiApplication([])
    view= QQuickView()
    view.setFlags(Qt.FramelessWindowHint)
    view.setSource("qrc:qml/qml/Progress.qml")
    view.show()
    app.exec()
#主函数
def OffAll():
    print("关闭")
if __name__  == '__main__':
    print(1)
    print(12)
    loadThread = multiprocessing.Process(name='loadThread',target=load)
    loadThread.start()
    atexit.register(OffAll)
    main(loadThread)
