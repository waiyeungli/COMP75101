from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from database.db import getDbRef
from event import getEvent

class MyAccountUpdateScreen(Screen):
    def on_pre_enter(self,*args):
        app = MDApp.get_running_app()
        self.title = app.myAccountScreenField
        self.ids.field_name.hint_text = app.myAccountScreenField
        field_val = getDbRef().child('useraccount/' + app.username + '/'+app.myAccountScreenField).get()
        if field_val:
            self.ids.field_name.text = field_val
        else:
            self.ids.field_name.text = ''
        print(app.myAccountScreenField, self.ids.field_name,field_val)
        return super().on_enter(*args)


    def save_button_click(self,input):
        app = MDApp.get_running_app()
        print(app.username,input.text,input.hint_text)
        if input.hint_text == 'Fund':
            current = getDbRef().child('useraccount/' + app.username + '/'+input.hint_text).get()
            newBalance = str(float(current)+float(input.text))
            getDbRef().child('useraccount/' + app.username + '/' + input.hint_text).set(newBalance)
        else:
            getDbRef().child('useraccount/' + app.username + '/' + input.hint_text).set(input.text)

        app.go_back()
    pass