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
            spacing: 40*(window.width/Screen.width)
            y:menuBar.y+30
            Row{
                spacing:30*(window.width/Screen.width)
                x:((window.width-2*image_width)-spacing)/2
                Item{    
                    width:image_width
                    height:width
                    Image{
                        id:input_img1
                        source: "qrc:/image/image/noimage.png"
                        width: image_width
                        height: width
                    }
                    Image{
                        id:input_img2
                        source: "qrc:/image/image/noimage.png"
                        width: image_width
                        height: width
                    }
                }
                Item{
                    width:10
                    height:10
                    Image{
                        id:output_img1
                        source: "qrc:/image/image/noimage.png"
                        width: image_width
                        height: width
                    }
                    Image{
                        id:output_img2
                        source: "qrc:/image/image/noimage.png"
                        width: image_width
                        height: width
                    }
                }
            }
            Row{
                spacing:70*(window.width/Screen.width)
                x:((window.width-7*button_width)-6*spacing)/2
                FluDropDownButton{
                    text:"选择相机"
                    id:camera_choose
                    width:button_width
                    FluMenuItem{
                        text:"相机1"
                        onClicked: {
                            camera_choose.text=text
                        }
                    }
                    FluMenuItem{
                        text:"相机2"
                        onClicked: {
                            camera_choose.text=text
                        }
                    }
                }
                FluDropDownButton{
                    text:"选择算法"
                    id:algorithm_choose
                    width:button_width
                    FluMenuItem{
                        text:"快速算法"
                        onClicked: {
                            algorithm_choose.text=text
                        }
                    }
                    FluMenuItem{
                        text:"分离算法"
                        onClicked: {
                            algorithm_choose.text=text
                        }
                    }
                }
                Repeater{
                    id:button_list
                    model:5
                    FluButton{
                        width:button_width
                        onClicked: {
                            if (index === 0) {
                                DetectControl.CameraControl()
                            }
                            if (index === 1) {
                                DetectControl.start()
                            }
                            if (index === 2) {
                                DetectControl.functionControl()
                            }
                            if (index === 3) {
                                DetectControl.outputImg()//为啥不从python直接调，因为测试不方便
                            }
                            if (index === 4) {
                                DetectControl.About()
                            }
                        }
                    }
                }
            }
            FluProgressBar{
                width:window.width
                height:20*(window.width/Screen.width)
            }
        }
    }
    Component.onCompleted: {
        button_list.itemAt(0).text="相机控制"
        button_list.itemAt(1).text="开始"
        button_list.itemAt(1).font.bold=true
        //button_list.itemAt(1).color="red"
        //family: "Arial" // 设置字体
        //font.pointSize: 16 // 设置字体大小
        button_list.itemAt(2).text="参数调整"
        button_list.itemAt(3).text="导出图片"
        button_list.itemAt(4).text="团队介绍"
    }
    Connections{
        target: DetectControl  // 指定连接的目标对象
        //function onGetCameraCC(){
        //    DetectControl.GetCameraCC([])
        //}
        function onImageData(ImgBase64) {
            output_img1.source = output_img2.source
            output_img2.source = "data:image/png;base64,"+ImgBase64
        }
        function onImageDataIn(ImgBase64) {
            input_img1.source = input_img2.source
            input_img2.source = "data:image/png;base64,"+ImgBase64
        }
    }
}