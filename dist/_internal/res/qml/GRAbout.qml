import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import FluentUI
import "qrc:///qml/qml"

FluWindow {

    id:window
    title:"团队介绍"
    width: 600
    height: 580
    fixSize: true
    launchMode: FluWindowType.SingleTask
    ColumnLayout{
        anchors{
            top: parent.top
            left: parent.left
            right: parent.right
        }
        RowLayout{
            Layout.topMargin: 20
            Layout.leftMargin: 15
            spacing: 14
            FluText{
                text:"OP之光"
                font: FluTextStyle.Title
            }
            FluText{
                text:"比赛专用版"
                font: FluTextStyle.Body
                Layout.alignment: Qt.AlignBottom
            }
        }
        RowLayout{
            spacing: 14
            Layout.topMargin: 20
            Layout.leftMargin: 15
            FluText{
                text:"软件作者："
            }
            FluText{
                text:"RIM"
                Layout.alignment: Qt.AlignBottom
            }
        }
        RowLayout{
            spacing: 14
            Layout.leftMargin: 15
            FluText{
                text:"GitHub:"
            }
            FluTextButton{
                id:text_hublink
                topPadding:0
                bottomPadding:0
                text:"https://github.com/RIM-9961?tab=repositories"
                Layout.alignment: Qt.AlignBottom
                onClicked: {
                    Qt.openUrlExternally(text_hublink.text)
                }
            }
        }
        RowLayout{
            spacing: 14
            Layout.leftMargin: 15
            FluText{
                text:"B站:"
            }
            FluTextButton{
                topPadding:0
                bottomPadding:0
                text:"https://space.bilibili.com/500709868?spm_id_from=333.1007.0.0"
                Layout.alignment: Qt.AlignBottom
                onClicked: {
                    Qt.openUrlExternally(text)
                }
            }
        }
        RowLayout{
            spacing: 14
            Layout.leftMargin: 15
            //FluText{
            //    id:text_info
            //    text:"开发不易，请作者喝杯咖啡吧！"
            //    ColorAnimation {
            //        id: animation
            //        target: text_info
            //       property: "color"
            //        from: "red"
            //        to: "blue"
            //        duration: 1000
            //        running: true
            //        loops: Animation.Infinite
            //        easing.type: Easing.InOutQuad
            //    }
            //}
        }
        RowLayout{
            spacing: 14
            Layout.topMargin: 20
            Layout.leftMargin: 15
            FluText{
                text:"工作室服务于的学校:"
            }
        }

        Item{
            Layout.preferredWidth: parent.width
            Layout.preferredHeight: 252
            Row{
                anchors.horizontalCenter: parent.horizontalCenter
                spacing: 30
                Image{
                    width: 250
                    height: 250
                    source: "qrc:/image/image/AHUT"
                }
            }
        }

        RowLayout{
            spacing: 14
            Layout.leftMargin: 15
            Layout.topMargin: 20
            FluText{
                id:text_desc
                text:"感谢您的支持！"
            }
        }
    }
}
