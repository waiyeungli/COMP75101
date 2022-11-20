from datetime import datetime, timezone
from kivymd.uix.button import MDRaisedButton
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from database.db import getDbRef, getStorageRef
import os

class AddProduct(Screen):
    def on_enter(self):
        app = MDApp.get_running_app()
        if app.image != None:
            ### Get the full path of the selected file
            file = app.image['files'][0]
            folder = app.image['folder']
            path = folder + '/' + file
            self.source = path
        else:
            self.soucre = ''
        print("Entering Add Product screen")
        return super().on_enter()

    def on_leave(self, *args):
        self.source = ''
        app = MDApp.get_running_app()
        app.image = None
        self.ids.product_category.text = ''
        self.ids.product_name.text = ''
        self.ids.product_description.text = ''
        self.ids.product_price.text = ''
        return super().on_leave(*args)

    def on_add_image_press(self):
        app = MDApp.get_running_app()
        app.show_screen('ImagePicker')

    def add_product(self,item):
        file = ''
        uniqueFilename =''
        if 'file' in item: # from localfile
            file =  item['file']['folder'] + '\\' + item['file']['files'][0]
            uniqueFilename = str(hex(int(datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S%f'))))[2:] + item['file']['files'][0]
        elif 'images' in item: #from remote
            file =  'image/' + item['images'][0]
            uniqueFilename = str(hex(int(datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S%f'))))[2:] + item['images'][0]

        bucket = getStorageRef()
        blob = bucket.blob(uniqueFilename)
        blob.upload_from_filename(file)
        blob.make_public()
        # location = file.replace('.', '_')
        create_dtm = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        myRef = getDbRef().child("products").push()
        app = MDApp.get_running_app()
        product = {
            "images":[uniqueFilename] ,
            "category": item["category"],
            "name": item["name"],
            "description": item["description"],
            "price": item['price'],
            "create_dtm":create_dtm,
            "create_by":app.username,
            "id":myRef.key,
            "status":"active"
        }
        myRef.set(product)
        user_products = getDbRef().child('useraccount').child(app.username).child('products').get()
        if user_products != None:
            user_products.append(product['id'])
            getDbRef().child('useraccount').child(app.username).child('products').set(user_products)
        else:
            user_products=[product['id']]
            getDbRef().child('useraccount').child(app.username).child('products').set(user_products)
        app.store = getDbRef().child("products").get()
        for key in app.store:
            item = app.store[key]
            isExist = os.path.exists('image/'+item['images'][0])
            if isExist:
                continue
            blob =  getStorageRef().blob(item['images'][0])
            try:
                blob.download_to_filename('image/'+item['images'][0])
            except:
                print('cannot find',item["images"][0])

    def on_add_product(self):
        app = MDApp.get_running_app()

        category = self.ids.product_category.text.strip()
        name = self.ids.product_name.text.strip()
        description = self.ids.product_description.text.strip()
        price = float(self.ids.product_price.text.strip())
        item ={"category":category,"name":name,"description":description,"price":price,"file":app.image}

        self.add_product(item);
        dialog = MDDialog(
            title = 'Thank You!',
            text = 'Upload Successful',
            buttons = [
                MDRaisedButton(
                    text = 'Close',
                    on_press = lambda x: self.dialog_close(dialog)),
            ]
        )
        self.dialog = dialog
        dialog.open()

    def dialog_close(self,instance):
        print(self,instance)
        self.dialog.dismiss()
        app = MDApp.get_running_app()
        app.go_back()