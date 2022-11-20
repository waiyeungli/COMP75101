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
from email_validator import validate_email, EmailNotValidError

from database.db import getDbRef


class Register(Screen):

    def button_back(self):
        app = MDApp.get_running_app()
        app.screenmanager.current = 'ScreenLogin'

    def button_clear(self):
        self.ids.txt_name.text = ""
        self.ids.txt_email.text = ""
        self.ids.txt_phone.text = ""
        self.ids.txt_address.text = ""
        self.ids.txt_username.text = ""
        self.ids.txt_password.text = ""
        self.ids.txt_repassword.text = ""

    def button_Reg(self):
        name = self.ids.txt_name.text
        email = self.ids.txt_email.text
        phone = self.ids.txt_phone.text
        address = self.ids.txt_address.text
        username = self.ids.txt_username.text
        password = self.ids.txt_password.text
        repassword = self.ids.txt_repassword.text

        if self.ids.txt_name.text == '':
            dialog = MDDialog(
                title='Alert',
                text='Please Enter Your Name.'
            )
            dialog.open()

        elif self.ids.txt_email.text == '':
            dialog = MDDialog(
                title='Alert',
                text='Please Enter Your Email.'
            )
            dialog.open()

        elif self.ids.txt_phone.text == '':
            dialog = MDDialog(
                title='Alert',
                text='Please Enter Your Phone Number.'
            )
            dialog.open()

        elif self.ids.txt_address.text == '':
            dialog = MDDialog(
                title='Alert',
                text='Please Enter Your Address.'
            )
            dialog.open()

        elif self.ids.txt_username.text == '':
            dialog = MDDialog(
                title='Alert',
                text='Please Enter Your Username.'
            )
            dialog.open()

        elif self.ids.txt_password.text == '':
            dialog = MDDialog(
                title='Alert',
                text='Please Enter Your Password.'
            )
            dialog.open()

        elif self.ids.txt_repassword.text == '':
            dialog = MDDialog(
                title='Alert',
                text='Please Re-enter Your Password.'
            )
            dialog.open()

        elif self.ids.txt_repassword.text == self.ids.txt_password.text:

            if len(self.ids.txt_phone.text) != 8:
                dialog = MDDialog(
                    title='Alert',
                    text='Your phone number is invalid. Phone number must be 8 digits.'
                )
                dialog.open()
            
            elif not validate_email(self.ids.txt_email.text):
                dialog = MDDialog(
                    title='Alert',
                    text='Your email is invalid.'
                )
                dialog.open()
                
            else:
                os.environ['SSL_CERT_FILE'] = certifi.where()
                cred_obj = firebase_admin.credentials.Certificate(
                    'comp7510-svc.json')

                firebase_admin.initialize_app(cred_obj, {
                    'databaseURL': 'https://comp7510-svc-default-rtdb.firebaseio.com/',
                    'storageBucket': 'comp7510-svc.appspot.com'
                })

                db_ref = db.reference('/')

                if username == db_ref.child('useraccount/' + username + '/username').get():
                    dialog = MDDialog(
                        title='Alert',
                        text='Username already exists.'
                    )
                    dialog.open()
                else:
                    db_ref.child('useraccount')
                    db_ref.child('useraccount/' + username + '/name').set(name)
                    db_ref.child('useraccount/' + username +
                                 '/email').set(email)
                    db_ref.child('useraccount/' + username +
                                 '/address').set(address)
                    db_ref.child('useraccount/' + username +
                                 '/phone').set(phone)
                    db_ref.child('useraccount/' + username +
                                 '/password').set(password)
                    db_ref.child('useraccount/' + username +
                                 '/username').set(username)

                    dialog = MDDialog(
                        title='Alert',
                        text='Successfully Registered'
                    )
                    dialog.open()

                    app = MDApp.get_running_app()
                    app.screenmanager.current = 'ScreenLogin'

        else:
            dialog = MDDialog(
                title='Alert',
                text='Password and Re-enter Password are inconsistent.'
            )
            dialog.open()


# If this file is not the starting file of the application, the following code will be ignored.
if __name__ == '__main__':
    from kivy.core.window import Window
    from kivy.utils import platform

    # Set window size if the app runs on Windows or MacOS
    if platform in ('win', 'macosx'):
        Window.size = (400, 800)

    class MyApp(MDApp):
        screenmanager = None

        # The app starts with a screen. The screen defination is loaded from the KV file
        def build(self):
            self.title = 'Registration'
            Builder.load_file('kv/page/reg.kv')
            Builder.load_file('kv/page/login.kv')

            self.screenmanager = ScreenManager()
            self.screenmanager.add_widget(Register(name='Register'))
            self.screenmanager.add_widget(ScreenLogin(name='ScreenLogin'))

            return self.screenmanager

    MyApp().run()
