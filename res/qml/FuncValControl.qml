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
    property var lock : 0
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
                    id:angle_data
                    text:"默认"
                    Layout.preferredWidth: 170
                    onTextChanged:{
                        if (lock!==0){
                            DetectControl.GetFunctionCC([angle_data.text,glblMax.value,glblMin.value,ezhcb.value,ztdx.value,xz1.text,xz2.text])
                        }                    }
                }
            }
        RowLayout{
                spacing: 10
                FluText{
                    text:"过滤比例(高)"
                    Layout.alignment: Qt.AlignVCenter
                }
                FluSlider{
                    id:glblMax
                    value: 0
                    from: 600
                    to:1500
                    onValueChanged:{
                        if (lock!==0){
                            DetectControl.GetFunctionCC([angle_data.text,glblMax.value,glblMin.value,ezhcb.value,ztdx.value,xz1.text,xz2.text])
                        }                    }
                }
        }
        RowLayout{
                spacing: 10
                FluText{
                    text:"过滤比例(低)"
                    Layout.alignment: Qt.AlignVCenter
                }
                FluSlider{
                    id:glblMin
                    value: 0
                    from: 0
                    to:40
                    onValueChanged:{
                        if (lock!==0){
                            DetectControl.GetFunctionCC([angle_data.text,glblMax.value,glblMin.value,ezhcb.value,ztdx.value,xz1.text,xz2.text])
                        }                    }
                }
        }
        RowLayout{
                spacing: 10
                FluText{
                    text:"二值化除比  "
                    Layout.alignment: Qt.AlignVCenter
                }
                FluSlider{
                    id:ezhcb
                    value: 0
                    onValueChanged:{
                        if (lock!==0){
                            DetectControl.GetFunctionCC([angle_data.text,glblMax.value,glblMin.value,ezhcb.value,ztdx.value,xz1.text,xz2.text])
                        }                    }
                }
        }
        RowLayout{
                spacing: 10
                FluText{
                    text:"字体大小     "
                    Layout.alignment: Qt.AlignVCenter
                }
                FluSlider{
                    id:ztdx
                    value: 0
                    onValueChanged:{
                        if (lock!==0){
                            DetectControl.GetFunctionCC([angle_data.text,glblMax.value,glblMin.value,ezhcb.value,ztdx.value,xz1.text,xz2.text])
                        }                    }
                }
        }
        RowLayout{
                spacing: 10
                FluText{
                    text:"对比度          "
                    Layout.alignment: Qt.AlignVCenter
                }
                FluTextBox{
                    id:xz1
                    Layout.preferredWidth: 170
                    onTextChanged:{
                        if (lock!==0){
                            DetectControl.GetFunctionCC([angle_data.text,glblMax.value,glblMin.value,ezhcb.value,ztdx.value,xz1.text,xz2.text])
                        }                    }
                }
        }
        RowLayout{
                spacing: 10
                FluText{
                    text:"锐化          "
                    Layout.alignment: Qt.AlignVCenter
                }
                FluTextBox{
                    id:xz2
                    Layout.preferredWidth: 170
                    onTextChanged:{
                        if (lock!==0){
                            DetectControl.GetFunctionCC([angle_data.text,glblMax.value,glblMin.value,ezhcb.value,ztdx.value,xz1.text,xz2.text])
                        }
                    }
            }
        }
        Component.onCompleted: {
            angle_data.text=DetectControl.GetFunctionCC([])[0]
            glblMax.value=DetectControl.GetFunctionCC([])[1]
            glblMin.value=DetectControl.GetFunctionCC([])[2]
            ezhcb.value=DetectControl.GetFunctionCC([])[3]
            ztdx.value=DetectControl.GetFunctionCC([])[4]
            xz1.value=DetectControl.GetFunctionCC([])[5]
            xz2.value=DetectControl.GetFunctionCC([])[6]
            lock=1
        }
        //Connections{
        //    target: DetectControl  // 指定连接的目标对象
        //    function onGetCameraCC(){
        //        DetectControl.GetCameraCC([baoguangtime.value,liangdu.value])
        //    }
        //    function onBaoGuangTime(num){
        //        baoguangtime.value=num
        //    }
        //}
    }
}
