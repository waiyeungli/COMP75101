from kivy.lang import Builder
from kivy.properties import DictProperty, StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.behaviors.touchripple import TouchRippleButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivymd.app import MDApp
from kivymd.uix.behaviors import RectangularElevationBehavior
from kivymd.uix.bottomnavigation import MDBottomNavigation
from kivymd.uix.gridlayout import MDGridLayout
from mandel_layouts import Column
from event import getEvent
from kivy.uix.screenmanager import Screen

Builder.load_file('kv/component/product_image.kv')
Builder.load_file('kv/component/product_list_item.kv')
Builder.load_file('kv/component/cart_list_item.kv')
Builder.load_file('kv/page/tab.kv')
Builder.load_file('kv/page/home.kv')
Builder.load_file('kv/page/cart.kv')
Builder.load_file('kv/page/my_acc.kv')
Builder.load_file('kv/page/my_acc_update.kv')
Builder.load_file('kv/page/detail.kv')
Builder.load_file('kv/page/explore.kv')
Builder.load_file('kv/page/order_status.kv')
Builder.load_file('kv/page/login.kv')
Builder.load_file('kv/page/add_product.kv')
Builder.load_file('kv/page/my_product.kv')
Builder.load_file('kv/page/image_picker.kv')
Builder.load_file('kv/page/container.kv')
Builder.load_file('kv/page/my_favourite.kv')
Builder.load_file('kv/page/reg.kv')




        #getDbRef().child(location).set(blob.public_url)



class LabelIconButton(TouchRippleButtonBehavior, Column):
    def on_press(self):
        print('pressed',self.parent.parent.parent.parent.on_order_status_press(self.text,self.field))
        return super(LabelIconButton, self).on_press()

class ProductCarouselImage(TouchRippleButtonBehavior,Image):
    item = DictProperty({})
    def on_press(self, *args):
        print("item press", self.item.name)
        #TODO:increment view count in firebase real time db
        getEvent().dispatch('on_detail_request', self.item)
        app = MDApp.get_running_app()
        #mandel's go back screen will not remove the instance of the widget
        #TODO: remove the existing MyAccountUpdateScreen widget from screenmanager if any <memory leak>
        app.detail = self.item
        app.show_screen("Detail")
        #app.screenmanager.current = "detail"


class ProductGridImage(TouchRippleButtonBehavior,Image):
    item = DictProperty({})
    def on_press(self, *args):
        print("item press", self.item.name)
        #TODO:increment view count in firebase real time db
        getEvent().dispatch('on_detail_request', self.item)
        app = MDApp.get_running_app()
        #mandel's go back screen will not remove the instance of the widget
        #TODO: remove the existing MyAccountUpdateScreen widget from screenmanager if any <memory leak>
        app.detail = self.item
        app.show_screen("Detail")
        #app.screenmanager.current = "detail"


class ExploreView(MDGridLayout):
    key = StringProperty("")
    name = StringProperty("")
    img = StringProperty("")
    description = StringProperty("")
    price = StringProperty("")



class ExploreViewElevated(ButtonBehavior,RectangularElevationBehavior,MDGridLayout):
    def on_press(self,*args):
        #getEvent().dispatch('on_detail_request', self.item)
        app = MDApp.get_running_app()
        app.detail = app.store[self.key]
        app.show_screen("Detail")
    key = StringProperty("")
    name = StringProperty("")
    img = StringProperty("")
    description = StringProperty("")
    price = StringProperty("")




class ProductListItem(ButtonBehavior, BoxLayout):

    item = DictProperty({})
    def on_press(self, *args):
        #TODO:increment view count in firebase real time db
        getEvent().dispatch('on_detail_request', self.item)
        app = MDApp.get_running_app()
        #mandel's go back screen will not remove the instance of the widget
        #TODO: remove the existing MyAccountUpdateScreen widget from screenmanager if any <memory leak>
        app.detail = self.item
        app.show_screen("Detail")
        #app.screenmanager.current = "detail"

class TabScreen(Screen):
    pass

class Container(Screen):
    pass

class CartListItem(ButtonBehavior, BoxLayout):
    item = DictProperty({})
    # def on_press(self, *args):
    #     #TODO:increment count from "Add to Cart" button?
    #     getEvent().dispatch('on_cart_request', self.item)
    #     app = MDApp.get_running_app()
    #     app.detail = self.item
    #     app.show_screen("Detail")
    #     #app.screenmanager.current = "detail"
    

class TotalListItem(ButtonBehavior, BoxLayout):
    item = DictProperty({})
    def on_press(self, *args):
        #TODO:increment count from "Add to Cart" button? on_cart_request? on_cart_update?
        getEvent().dispatch('on_cart_request', self.item)
        app = MDApp.get_running_app()
        #mandel's go back screen will not remove the instance of the widget
        app.detail = self.item
        app.show_screen("Detail")
        #app.screenmanager.current = "detail"

class MyMDBottomNavigation(MDBottomNavigation):

    def __init__(self, **kwargs):
        app = MDApp.get_running_app()
        app.tab = self
        super(MyMDBottomNavigation, self).__init__(**kwargs)

    def on_tab_touch_down(self, num):
        self.ids.tab_manager.transition.duration = 0.0001
