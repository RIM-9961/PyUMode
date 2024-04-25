import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Layouts
import Qt.labs.platform
import FluentUI
import "qrc:///qml/qml"
FluWindow{
    id:window
    title: "缺口长度检测"
    width: Screen.width *0.63
    height: Screen.width*0.63 /1.6
    minimumWidth: 520
    minimumHeight: 520/1.6+50
    launchMode: FluWindowType.SingleTask
    appBar: FluAppBar {
        id:appbar
        visible:false
    }
    SettingsViewModel{
        id:viewmodel_settings
    }
    SystemTrayIcon {
        id:system_tray
        visible: true
        icon.source: "qrc:/image/image/favicon.ico"
        tooltip: "缺口长度检测"
        menu: Menu {
            MenuItem {
                text: "退出"
                onTriggered: {
                    FluApp.exit()
                }
            }
        }
        onActivated:
            (reason)=>{
                if(reason === SystemTrayIcon.Trigger){
                    window.show()
                    window.raise()
                    window.requestActivate()
                }
            }
    }
    FluContentDialog{
        id:dialog_close
        title:"退出"
        message:"确定要退出程序吗？"
        negativeText:"最小化"
        buttonFlags: FluContentDialogType.NegativeButton | FluContentDialogType.NeutralButton | FluContentDialogType.PositiveButton
        onNegativeClicked:{
            window.hide()
            system_tray.showMessage("友情提示","缺口长度检测已隐藏至托盘,点击托盘可再次激活窗口");
        }
        positiveText:"退出"
        neutralText:"取消"
        onPositiveClicked:{
            FluApp.exit(0)
        }
    }
    Component{
        id:nav_item_right_menu
        FluMenu{
            id:menu
            width: 130
            FluMenuItem{
                text: "在独立窗口打开"
                visible: true
                onClicked: {
                    FluApp.navigate("/pageWindow",{title:modelData.title,url:modelData.url})
                }
            }
        }
    }
    Flipable{
        id:flipable
        anchors.fill: parent
        property bool flipped: false
        property real flipAngle: 0
        transform: Rotation {
            id: rotation
            origin.x: flipable.width/2
            origin.y: flipable.height/2
            axis { x: 0; y: 1; z: 0 }
            angle: flipable.flipAngle
        }
        states: State {
            PropertyChanges { target: flipable; flipAngle: 180 }
            when: flipable.flipped
        }
        transitions: Transition {
            NumberAnimation { target: flipable; property: "flipAngle"; duration: 1000 ; easing.type: Easing.OutCubic}
        }
        back: Item{
            anchors.fill: flipable
            visible: flipable.flipAngle !== 0
            FluAppBar {
                anchors {
                    top: parent.top
                    left: parent.left
                    right: parent.right
                }
                z:7
                closeClickListener: ()=>{dialog_close.open()}
            }
            Row{
                z:8
                anchors{
                    top: parent.top
                    left: parent.left
                    topMargin: FluTools.isMacos() ? 20 : 5
                    leftMargin: 5
                }
                FluIconButton{
                    iconSource: FluentIcons.ChromeBack
                    width: 30
                    height: 30
                    iconSize: 13
                    onClicked: {
                        flipable.flipped = false
                    }
                }
            }
        }
        front: Item{
            id:page_front
            visible: flipable.flipAngle !== 180
            anchors.fill: flipable
            FluAppBar {
                id:app_bar_front
                anchors {
                    top: parent.top
                    left: parent.left
                    right: parent.right
                }
                closeClickListener: ()=>{dialog_close.open()}
                z:7
            }
            FluNavigationView{
                property int clickCount: 0
                id:nav_view
                width: parent.width
                height: parent.height
                z:999
                //Stack模式，每次切换都会将页面压入栈中，随着栈的页面增多，消耗的内存也越多，内存消耗多就会卡顿，这时候就需要按返回将页面pop掉，释放内存。该模式可以配合FluPage中的launchMode属性，设置页面的启动模式
                //                pageMode: FluNavigationViewType.Stack
                //NoStack模式，每次切换都会销毁之前的页面然后创建一个新的页面，只需消耗少量内存，可以配合FluViewModel保存页面数据（推荐）
                pageMode: FluNavigationViewType.NoStack
                items : GRMainList
                footerItems:GRItemsFooter
                topPadding:FluTools.isMacos() ? 20 : -4
                displayMode:viewmodel_settings.displayMode
                logo: "qrc:/image/image/favicon.ico"
                title:"缺口长度检测"
                Component.onCompleted: {
                    GRMainList.navigationView = nav_view
                    GRMainList.paneItemMenu = nav_item_right_menu
                    GRItemsFooter.navigationView = nav_view
                    GRItemsFooter.paneItemMenu = nav_item_right_menu
                    setCurrentIndex(0)
                }
            }
        }
    }
}