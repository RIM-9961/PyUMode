import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Layouts
import Qt.labs.platform
Item {
        width: Screen.width*0.5
        height: width*0.5
        AnimatedImage  {
            id: gifImage
            source: "qrc:/image/image/mrs.gif" // 替换为你的GIF文件路径
            anchors.fill: parent
            fillMode: Image.PreserveAspectFit
            asynchronous: true
            width: parent.width 
            height: parent.height 
        }
    }