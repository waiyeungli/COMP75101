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


# class CartListItem(Screen):
#     item = DictProperty({})
#     def AddQuantity (self)
#         item_quantity = self.bttn_clicks
#         item_quantity += 1
#         print("You have selected " + root.item["name"] + str(item_quantity) + "times")

#     def DeleteItem (self)

