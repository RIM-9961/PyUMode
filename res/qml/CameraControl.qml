import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Layouts
import Qt.labs.platform
import FluentUI
Window{
    id:root
    width:500
    height:Screen.height
    Image{
        id:im1
        width:root.width
        height:root.height
        anchors.centerIn: parent
        source: "C:/Users/10644/Desktop/1.jpg"
    }
    FluButton{
        onClicked:{
            im1.source = "C:/Users/10644/Desktop/2.jpg"
            //im1.source = "C:/Users/10644/Desktop/3.jpg"
            //im1.source = "C:/Users/10644/Desktop/4.jpg"
            //im1.source = "C:/Users/10644/Desktop/5.jpg"
        }
    }
    Gird{
    Row{
        spacing: 10
        FluentButton{
            
        }
        FluentButton{
            
        }
    }
    }
    Column{}
    Girdlayout{    }
}