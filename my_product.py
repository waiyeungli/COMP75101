from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from database.db import getDbRef
from index import ProductListItem

class MyProductScreen(Screen):
    def on_pre_enter(self, *args):
        app = MDApp.get_running_app()
        user = getDbRef().child(f'useraccount/{app.username}').get()
        if 'products' in user:
            for key in user['products']:
                self.ids.column.add_widget(ProductListItem(item=app.store[key]))
        return super().on_enter(*args)
    def on_leave(self, *args):
        self.ids.column.clear_widgets()
        return super().on_leave(*args)