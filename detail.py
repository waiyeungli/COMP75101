from kivymd.uix.button import MDRaisedButton
from kivy.properties import DictProperty
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from database.db import getDbRef


class DetailScreen(Screen):
    #right_action_items = 'heart'
    item = DictProperty({})
    def on_trash(self):
        print('on trash',self.item)
        dialog = MDDialog(
        title = 'Are you sure delete this item?',
        text = 'This action is non reversible',
        buttons = [
            MDRaisedButton(
                text = 'Yes',
                on_press = lambda x: self.on_confirm_trash(dialog)),
            MDRaisedButton(
                text = 'No',
                on_press = lambda x: dialog.dismiss()),
            ]
        )
        dialog.open()


    def on_confirm_trash(self,dialog):
        dialog.dismiss()
        app = MDApp.get_running_app()
        #avoid sql injection style's query injection
        create_by = getDbRef().child('products').child(self.item['id']).child('create_by').get()
        if create_by == app.username:
            getDbRef().child('products').child(self.item['id']).child('status').set('deleted')
            user_products = getDbRef().child('useraccount').child(app.username).child('products').get()
            if user_products != None:
                user_products.remove(self.item['id'])
                getDbRef().child('useraccount').child(app.username).child('products').set(user_products)
                app.go_back()
        else:
            dialog = MDDialog(
            title = 'Error',
            text = 'This product is not own by you',
            buttons = [
                MDRaisedButton(
                    text = 'Close',
                    on_press = lambda x: dialog.dismiss()),
                ]
            )
            dialog.open()

    def on_like(self):
        app = MDApp.get_running_app()
        user_like = getDbRef().child('useraccount').child(app.username).child('like').get()
        if user_like != None:
            if self.item['id'] in user_like:
                user_like.remove(self.item['id'])
                self.ids.topBar.right_action_items = [["cards-heart-outline", lambda x: self.on_like()]]
            else:
                user_like.append(self.item['id'])
                self.ids.topBar.right_action_items = [["cards-heart", lambda x: self.on_like()]]
        else:
            user_like=[self.item['id']]
            self.ids.topBar.right_action_items = [["cards-heart", lambda x: self.on_like()]]
        getDbRef().child('useraccount').child(app.username).child('like').set(user_like)


    def on_pre_enter(self):
        app = MDApp.get_running_app()
        #self.isTrash = len(app.screenmanager.children) >=2 and app.screenmanager.children[1].name == 'MyProductScreen'
        self.item = app.detail
    # def on_pre_enter(self):
    #    app = MDApp.get_running_app()
        if  'MyProductScreen' in app.last_screens:
            #right_action_items: [["trash-can-outline", lambda x: root.on_trash()]] if root.right_action_items == 'trash' else [["cards-heart", lambda x: root.on_like()]]
            self.ids.topBar.right_action_items = [["trash-can-outline", lambda x: self.on_trash()]]
            #self.right_action_items = 'trash'
        else:
            #self.right_action_items = 'heart'
            user_like = getDbRef().child('useraccount').child(app.username).child('like').get()
            if user_like != None and self.item['id'] in user_like:
                self.ids.topBar.right_action_items = [["cards-heart", lambda x: self.on_like()]]
            else:
                self.ids.topBar.right_action_items = [["cards-heart-outline", lambda x: self.on_like()]]

