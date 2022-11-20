import os
from os.path import dirname, join
from kivymd.uix.label import MDLabel
from image_picker import ImagePicker
#from kivy.uix.boxlayout import BoxLayout
from kivy.config import Config
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.loader import Loader
from kivy.metrics import Metrics
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.utils import platform
from kivymd.app import MDApp
from kivymd.uix.bottomnavigation import MDBottomNavigation
import constant
from add_product import AddProduct
from login import ScreenLogin
from database.db import getDbRef, getStorageRef
from event import getEvent
from index import *
from index import TabScreen
from cart import CartScreen
from my_account_update import MyAccountUpdateScreen
from my_favourite import MyFavouriteScreen
from order_status import OrderStatusScreen
from my_product import MyProductScreen
from home import HomeScreen
from explore import ExploreScreen
from my_account import MyAccountScreen
from detail import DetailScreen
from cart import CartScreen
from reg import Register
import json

# ScreenManager().add_widget(BottomNavigationWindow(name='BottomNav'))
class Main(MDApp):
    bgColor = constant.BG_COLOR
    detail_page_item = {}
    width = Window.width / Metrics.density
    height = Window.height / Metrics.density
    kv_directory = join(dirname(__file__), 'kv')
    db = getDbRef()
    tab = {}
    bucket = getStorageRef()
    store = []
    display_store =[]
    user = {}
    username=''
    try:
        user = json.load(open('user.json'))
        username = user["username"]
    except:
        user = {}
        username=''


    image = None
    # for screen control
    screenmanager = None
    last_screens = []

    def on_start(self):
        store = self.db.child("products").get()
        #TODO: should be implement in a AsyncCacheImage Component instead of download in advance
        for key in store:
            item = store[key]
            isExist = os.path.exists('image/'+item['images'][0])
            if isExist:
                continue
            blob = self.bucket.blob(item['images'][0])
            try:
                blob.download_to_filename('image/'+item['images'][0])
            except:
                print('cannot find',item["images"][0])
        ev = getEvent()
        self.store = store
        display_store = {k: v for k, v in store.items() if 'status' not in v or v['status'] !='deleted'}
        #dict(filter(lambda (k,v): 'status' in v and v['status']!='deleted', store.items()))
        ev.dispatch('on_product_update', display_store)


        # self.dispatch('on_product_update',store);
        # self.update_carousel(store)
        # for item in store:
        #     print(item['name'])
        return super().on_start()

    def show_screen(self, screen_name):
        self.last_screens.append(self.screenmanager.current)
        self.screenmanager.transition.direction = 'left'
        if screen_name in self.screenmanager.screen_names:
            self.screenmanager.current = screen_name
        else:
            #dynamic load page to reduce start up time
            if screen_name == "MyFavouriteScreen":
                self.screenmanager.add_widget(MyFavouriteScreen(name="MyFavouriteScreen"))
            elif screen_name == "ImagePicker":
                self.screenmanager.add_widget(ImagePicker(name="ImagePicker"))
            elif screen_name == "MyAccountUpdateScreen":
                self.screenmanager.add_widget(MyAccountUpdateScreen(name="MyAccountUpdateScreen"))
            elif screen_name == "OrderStatusScreen":
                self.screenmanager.add_widget(OrderStatusScreen(name="OrderStatusScreen"))
            elif screen_name == "AddProduct":
                self.screenmanager.add_widget(AddProduct(name="AddProduct"))
            elif screen_name == "MyProductScreen":
                self.screenmanager.add_widget(MyProductScreen(name="MyProductScreen"))
            elif screen_name == "Detail":
                self.screenmanager.add_widget(DetailScreen(name="Detail"))
            self.screenmanager.current = screen_name

    def go_back(self):
        screen_name = self.last_screens.pop()
        self.screenmanager.transition.direction = 'right'
        self.screenmanager.current = screen_name

    def on_resize(self, *args):
        #print("width", self,args,args[1],args[1][0])
        if (args[1][0] > 600):
            if self.tab.ids.tab1.children[0].ids.my_layout.cols == 1:
                if not self.tab.ids.tab1.children[0].isSearching:
                    self.tab.ids.tab1.children[0].ids.my_layout.cols = 2
        else:
            if self.tab.ids.tab1.children[0].ids.my_layout.cols == 2:
                self.tab.ids.tab1.children[0].ids.my_layout.cols = 1

    def build(self):
        height = 800
        width = 400
        if platform in ('win'):
            height = 800
            width = 400
        elif platform in ('macosx'):
            height = 300
            width = 150

        Config.set('graphics', 'height', height)
        Config.set('graphics', 'width', width)
        Config.write()
        Window.size = (width,height)
        Window.minimum_width, Window.minimum_height = Window.size
        Loader.loading_image = 'image/loading.png'
        #Config.read("main.ini")
        self.title = 'HomeScreen'
        self.screenmanager = ScreenManager()

        self.screenmanager.add_widget(Register(name="Register"))
        self.screenmanager.add_widget(TabScreen(name="TabScreen"))
        self.screenmanager.add_widget(ScreenLogin(name='ScreenLogin'))
        container = self.create_username_container()




        # self.screenmanager.add_widget(ChangeScreen3(name='ChangeScreen3'))

        Window.bind(size=self.on_resize)
        return container #self.screenmanager

    #for the requirement of having a username on every page
    def create_username_container(self):
        if  self.username == "":
            self.screenmanager.current = 'ScreenLogin'
        else:
            self.screenmanager.current = 'TabScreen'
        container = Container()
        container.ids.layout1.add_widget(self.screenmanager)
        if self.username !='':
            username_text = "Welcome " + self.username +" !! (My Login Name)"
        else:
            username_text = ''
        label = MDLabel(text=username_text,pos_hint={'top':1}, padding=('10dp',0) ,height='18dp',size_hint=(1, None))
        label.font_size='12dp'
        label.text_color= (0.8,0.8,0.8,0.5)
        container.ids.layout1.add_widget(label)
        return container


Main().run()
