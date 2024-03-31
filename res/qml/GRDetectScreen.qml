import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Layouts
import Qt.labs.platform
import FluentUI
FluArea{
    property var image_width : window.width/2-40*(window.width/Screen.width)
    property var button_width : window.width/7-90*(window.width/Screen.width)
    id:root
    width: window.width
    height: window.height
    y: -6
    FluMenuBar{
        id:menuBar
        FluMenu{
            title:qsTr("文件")
            Action { text: qsTr("新建...") }
            FluMenu{
                        title: "导出为..."
                        Action { text: qsTr("工程文件") }
                        Action { text: qsTr("数据文件") }
                    }
            }
        FluMenu{
            title:qsTr("设置")
            Action { text: qsTr("输出管理") }
            Action { text: qsTr("脚本管理") }
            FluMenuSeparator { }
            Action { text: qsTr("界面管理") }
            Action { text: qsTr("快捷键设置") }
            }
        FluMenu{
            title:qsTr("相机")
            Action { text: qsTr("相机定位") }
            Action { text: qsTr("相机参数") }
            }
        FluMenu{
            title:qsTr("帮助")
            Action { text: qsTr("去网上搜") }
            Action { text: qsTr("检查更新") }
            FluMenuSeparator { }
            Action { text: qsTr("关于") }
            }
    }
    Item{
        Column{
            spacing: 15
            y:menuBar.y+30
            Row{
                spacing:30*(window.width/Screen.width)
                x:((window.width-2*image_width)-spacing)/2
                Image{
                    source: "qrc:/image/image/noimage.png"
                    width: image_width
                    height: width
                }
                Image{
                    source: "qrc:/image/image/noimage.png"
                    width: image_width
                    height: width
                }
            }
            Row{
                spacing:10*(window.width/Screen.width)
                x:((window.width-7*button_width)-6*spacing)/2
                FluDropDownButton{
                    text:"选择相机"
                    id:camera_choose
                    width:button_width
                    FluMenuItem{
                        text:"相机1"
                        onClicked: {
                            camera_choose.text = text
                        }
                    }
                    FluMenuItem{
                        text:"相机2"
                        onClicked: {
                            camera_choose.text = text
                        }
                    }
                }
                FluDropDownButton{
                    text:"选择算法"
                    width:button_width
                }
                Repeater{
                    id:button_list
                    model:5
                    FluButton{
                        width:button_width
                    }
                }
            }
            FluProgressBar{
                width:window.width
            }
        }
    }
    Component.onCompleted: {
        button_list.itemAt(0).text = "相机控制"
        button_list.itemAt(1).text = "开始"
        button_list.itemAt(2).text = "参数调整"
        button_list.itemAt(3).text = "导出图片"
        button_list.itemAt(4).text = "团队介绍"
    }
     Connections{
        target: DetectControl  // 指定连接的目标对象
    }
}