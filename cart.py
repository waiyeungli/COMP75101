from datetime import datetime, timezone
from os.path import dirname, join
from kivymd.uix.button import MDRaisedButton
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import Metrics
from kivy.properties import DictProperty, NumericProperty, StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.behaviors.touchripple import TouchRippleButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.recycleview import RecycleView
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.app import MDApp
from kivymd.uix.behaviors import RectangularElevationBehavior
from kivymd.uix.bottomnavigation import MDBottomNavigation
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from mandel_layouts import Column
from kivymd.uix.dialog import MDDialog
import constant
from database.db import getDbRef, getStorageRef
from event import getEvent
from index import CartListItem
#from tkinter import *


class CartScreen(Screen):
    item = DictProperty({})
    def __init__(self, **kwargs):
        print('binding on cart event')
        ev = getEvent()
        #TODO update the event name (on_product_update -> on_cart_update)
        ev.bind(on_product_update=self.fillCart)
        super(CartScreen, self).__init__(**kwargs)

    def fillCart(self, event, store):
        #TODO have to agree Dictionary object
        byName = sorted(store, key=lambda x: store[x]["name"], reverse=True)
        for k in byName[:4]:
            #TODO 
            self.ids.shopping_cart.add_widget(CartListItem(item=store[k]))
        #TODO
        #self.ids.shopping_cart.add_widget(TotalListItem(item=item))
    
    def on_pre_enter(self, *args):
        app = MDApp.get_running_app()
        CartItem = getDbRef().child(f'useraccount/{app.username}/CartItem').get()
        if CartItem != None:
            for key in CartItem:
                self.ids.shopping_cart.add_widget(CartListItem(item=app.store[key]))
        return super().on_enter(*args)

    # def on_leave(self, *args):
    #     self.ids.shopping_cart.clear_widgets()
    #     return super().on_leave(*args)

    def show_dialog(self):
        dialog = MDDialog( 
            title = 'Checkout',
            text = 'Thank you for purchasing. We will confirm the order and deliver the items to you shortly.',
            buttons = [ 
                MDRaisedButton(
                    text = 'See Order',
                    on_press = lambda x: print(x.text)), #Print purchased item names
                MDRaisedButton(
                    text = 'Close',
                    on_press = lambda x: dialog.dismiss()),
                    #TODO: Send orders to my account & clear CartListItem
            ] 
        )
        dialog.open()

class DetailScreen(Screen):
    def fillCart (self):
        self.bttn_clicks = 0
        self.update_quantity()

    def update_quantity(self):
        self.bttn_clicks += 1
        print("Total Clicks: " + str(self.bttn_clicks))

# sm = ScreenManager()
# cartscreen = CartScreen(name='shopping_cart')
# detailscreen = DetailScreen(name='details')
# sm.add_widget(cartscreen)
# sm.add_widget(detailscreen)

