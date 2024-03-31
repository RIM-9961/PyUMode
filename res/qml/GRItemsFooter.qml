pragma Singleton
import QtQuick
import FluentUI
FluObject{
    property var navigationView
    property var paneItemMenu
    id:footer_items
    FluPaneItemSeparator{}
    FluPaneItem{
        title:"关于"
        icon:FluentIcons.Contact
        onTapListener:function(){
            DetectControl.About()
        }
    }
}
