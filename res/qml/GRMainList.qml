pragma Singleton
import QtQuick
import FluentUI
FluObject {
    property var navigationView
    property var paneItemMenu
    function rename(item, newName){
        if(newName && newName.trim().length>0){
            item.title = newName;
        }
    }
    FluPaneItem{
        id:item_detect
        count: 0
        title:"双目探测计算"
        menuDelegate: paneItemMenu
        infoBadge:FluBadge{
            count: item_detect.count
        }
        url:"qrc:/qml/qml/GRDetectScreen.qml"
        onTap:{
            if(navigationView.getCurrentUrl()){
                item_detect.count = 0
            }
            navigationView.push(url)
        }
    }
    FluPaneItem{
        id:item_laser
        count: 0
        title:"激光剪切干涉计算"
        menuDelegate: paneItemMenu
        infoBadge:FluBadge{
            count: item_laser.count
        }
        url:"qrc:/qml/qml/HotloadWindow.qml"
        onTap:{
            if(navigationView.getCurrentUrl()){
                item_laser.count = 0
            }
            navigationView.push(url)
        }
    }
    function getRecentlyAddedData(){
        var arr = []
        for(var i=0;i<children.length;i++){
            var item = children[i]
            if(item instanceof FluPaneItem && item.recentlyAdded){
                arr.push(item)
            }
            if(item instanceof FluPaneItemExpander){
                for(var j=0;j<item.children.length;j++){
                    var itemChild = item.children[j]
                    if(itemChild instanceof FluPaneItem && itemChild.recentlyAdded){
                        arr.push(itemChild)
                    }
                }
            }
        }
        arr.sort(function(o1,o2){ return o2.order-o1.order })
        return arr
    }
    function getRecentlyUpdatedData(){
        var arr = []
        var items = navigationView.getItems();
        for(var i=0;i<items.length;i++){
            var item = items[i]
            if(item instanceof FluPaneItem && item.recentlyUpdated){
                arr.push(item)
            }
        }
        return arr
    }
    function getSearchData(){
        if(!navigationView){
            return
        }
        var arr = []
        var items = navigationView.getItems();
        for(var i=0;i<items.length;i++){
            var item = items[i]
            if(item instanceof FluPaneItem){
                if (item.parent instanceof FluPaneItemExpander)
                {
                    arr.push({title:`${item.parent.title} -> ${item.title}`,key:item.key})
                }
                else
                    arr.push({title:item.title,key:item.key})
            }
        }
        return arr
    }
    function startPageByItem(data){
        navigationView.startPageByItem(data)
    }
    Component.onCompleted: {
    }
}
