import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import FluentUI
import "qrc:///qml/qml"

FluWindow {
    id:window
    title:"参数调整"
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
                    text:"图片旋转角度"
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
                    text:"过滤比例(高)"
                    Layout.alignment: Qt.AlignVCenter
                }
                FluSlider{
                    id:slider_text_size
                    value: 0
                    from: 600
                    to:1500
                }
        }
        RowLayout{
                spacing: 10
                FluText{
                    text:"过滤比例(低)"
                    Layout.alignment: Qt.AlignVCenter
                }
                FluSlider{
                    id:slider_gap_x
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
    }
}
