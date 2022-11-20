from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from database.db import getDbRef
from event import getEvent
from index import ProductListItem

class MyFavouriteScreen(Screen):
    def on_pre_enter(self, *args):
        app = MDApp.get_running_app()
        like = getDbRef().child(f'useraccount/{app.username}/like').get()
        if like != None:
            for key in like:
                self.ids.column.add_widget(ProductListItem(item=app.store[key]))
        return super().on_enter(*args)
    def on_leave(self, *args):
        self.ids.column.clear_widgets()
        return super().on_leave(*args)