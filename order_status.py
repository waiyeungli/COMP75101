from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from database.db import getDbRef
from event import getEvent
from index import ProductListItem

class OrderStatusScreen(Screen):
    name = StringProperty("")
    def on_pre_enter(self):
        app = MDApp.get_running_app()
        self.title = app.myAccountScreenTitle
        self.ids.column.clear_widgets()
        itemIds = getDbRef().child('useraccount/' + app.username + '/order/'+app.myAccountScreenField).get()
        #itemIds = [1,3,5,6]
        if itemIds == None:
            self.ids.column.add_widget(MDLabel(size_hint_y=None,height=100,text=f"You have no {app.myAccountScreenField} orders.",halign='center'))
        else:
            for item in itemIds:
                key = str(item)
                if key in app.store:
                    self.ids.column.add_widget(ProductListItem(item=app.store[key]))
        print("OrderStatusScreen on_order_status_press",app.myAccountScreenTitle,app.myAccountScreenField,itemIds)