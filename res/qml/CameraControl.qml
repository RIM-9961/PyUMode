import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import FluentUI
import "qrc:///qml/qml"

FluWindow {
    id:window
    title:"相机控制"
    width: 300
    height: 300
    fixSize: true
    launchMode: FluWindowType.SingleTask
    Loader {
        id: myLoader
        anchors.centerIn: parent
    }
    ColumnLayout{
        anchors{
            left: parent.left
            leftMargin: 14
        }
        RowLayout{
                spacing: 10
                Layout.topMargin: 14
                FluText{
                    text:"不知道写些什么"
                    Layout.alignment: Qt.AlignVCenter
                }
                FluTextBox{
                    id:text_box
                    text:"默认"
                    Layout.preferredWidth: 170
                }
            }
        RowLayout{
                spacing: 10
                FluText{
                    text:"曝光时间     "
                    Layout.alignment: Qt.AlignVCenter
                }
                FluSlider{
                    id:baoguangtime
                    value: 0
                    from: 0
                    to:10000
                }
        }
        RowLayout{
                spacing: 10
                FluText{
                    text:"亮度调整     "
                    Layout.alignment: Qt.AlignVCenter
                }
                FluSlider{
                    id:liangdu
                    value: 0
                    from: 0
                    to:40
                }
        }
        RowLayout{
                spacing: 10
                FluText{
                    text:"二值化除比  "
                    Layout.alignment: Qt.AlignVCenter
                }
                FluSlider{
                    id:slider_gap_y
                    value: 0
                }
        }
        RowLayout{
                spacing: 10
                FluText{
                    text:"字体大小     "
                    Layout.alignment: Qt.AlignVCenter
                }
                FluSlider{
                    id:slider_offset_x
                    value: 0
                }
        }
        RowLayout{
                spacing: 10
                FluText{
                    text:"闲置1          "
                    Layout.alignment: Qt.AlignVCenter
                }
                FluSlider{
                    id:slider_offset_y
                    value: 0
                }
        }
        RowLayout{
                spacing: 10
                FluText{
                    text:"闲置2          "
                    Layout.alignment: Qt.AlignVCenter
                }
                FluSlider{
                    id:slider_rotate
                    value: 0
                    from: 0
                    to:360
            }
        }
        Component.onCompleted: {
        }
        Connections{
            target: DetectControl  // 指定连接的目标对象
            function onGetCameraCC(){
                DetectControl.GetCameraCC([baoguangtime.value,liangdu.value])
            }
        }
    }
}
