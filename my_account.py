from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from event import getEvent


class MyAccountScreen(Screen):
    def on_my_acc_update(self, field):
        print('on_my_acc_update',field)
        app = MDApp.get_running_app()
        app.myAccountScreenField = field
        #getEvent().dispatch('on_my_acc_update', field)
        app.show_screen('MyAccountUpdateScreen')
        print(self)

    def on_order_status_press(self,title,field):
        print('on_order_status_press',title,field)
        app = MDApp.get_running_app()
        app.myAccountScreenField = field
        app.myAccountScreenTitle = title
        app.show_screen('OrderStatusScreen')