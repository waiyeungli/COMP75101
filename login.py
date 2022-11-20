import firebase_admin
from firebase_admin import db
from firebase_admin import storage
import certifi
import os

from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivymd.uix.dialog import MDDialog
from tkinter import dialog
from kivymd.app import MDApp
from kivy.app import Builder
from reg import Register

from database.db import getDbRef

class ScreenLogin(Screen):
    
    def Register(self):
        app = MDApp.get_running_app()
        app.screenmanager.current = 'Register'


    def logger(self):
        user = self.ids.txt_user.text
        password = self.ids.txt_password.text

        user = user.strip()

        if len(user) == 0 or len(password) == 0:
            dialog = MDDialog(
                                title = 'Alert',
                                text = 'Please enter your username / password.'
                             )
            dialog.open()
        else:
            db_ref = getDbRef()
            db_user = db_ref.child('useraccount/'+ user + '/username').get()
            db_pw = db_ref.child('useraccount/'+ user + '/password').get()

            print (db_user, db_pw)

            if user == db_user and password == db_pw:
                print (db_user, db_pw)
                
                loginSuccess = True
                if loginSuccess:
                    print (user, password)
                    app = MDApp.get_running_app()
                    app.user = db_ref.child("useraccount/"+user).get()
                    app.username = user
                    app.screenmanager.current = 'TabScreen'

            else:
                dialog = MDDialog(
                                title = 'Alert',
                                text = 'Your username or password is incorrect.'
                             )
                dialog.open()

    def clear(self):
        self.ids.txt_user.text = ""
        self.ids.txt_password.text = ""


if __name__ == '__main__':
    from kivy.core.window import Window
    from kivy.utils import platform

    if platform in ('win', 'macosx'):
        Window.size = (400, 800)

    class MyApp(MDApp): 
        screenmanager = None

        def build(self):
            self.title = 'Login'
            Builder.load_file('kv/page/login.kv')
            Builder.load_file('kv/page/reg.kv')
        
            self.screenmanager = ScreenManager()
            self.screenmanager.add_widget(ScreenLogin(name='ScreenLogin'))
            self.screenmanager.add_widget(Register(name='Register'))

            return self.screenmanager


    MyApp().run()