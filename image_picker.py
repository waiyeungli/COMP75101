from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp

class ImagePicker(Screen):
    def on_enter(self):
        print("Entering ImagePicker screen")
    def on_image_chosen(self):
        manager = self.ids.manager
        selected = manager.get_selected()
        app = MDApp.get_running_app()
        print('selected',selected)
        if len(selected['files']) != 0:
            app.image = selected
        else:
            app.image = None
        app.go_back()