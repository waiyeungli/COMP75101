from kivy.event import EventDispatcher
from kivymd.app import MDApp
eventRef = False
#To achieve DRY (Dont Repeat Yourself), let's create a singlton function to hold the connection


def getEvent():
    global eventRef
    if not eventRef:
        eventRef = GlobalEventDispatcher()
    return eventRef

#To register a event
# 1. add a default handler, return false to propagate the event
# 2. register event here
class GlobalEventDispatcher(EventDispatcher):
    def __init__(self, **kwargs):
         self.register_event_type('on_product_update')
         self.register_event_type('on_detail_request')
         self.register_event_type('on_cart_update')
         self.register_event_type('on_cart_request')
         self.register_event_type('on_my_acc_update')
         self.register_event_type('on_order_status_press')

         super(GlobalEventDispatcher, self).__init__(**kwargs)

    def on_my_acc_update(self, field):
        print("Event: on_my_acc_update",field)

    def on_order_status_press(self,title,field):
        print("Event: on_order_status_press",title,field)

    def on_product_update(self, store):
        app = MDApp.get_running_app()
        app.store = store
        print("Event: on_product_update product retrieved from google firebase successfully, total " ,len(store)," items" );

    def on_detail_request(self, item):
        print("Event: on_detail_request A detail page is requested for item " ,item.name);
    
    def on_cart_update(self, store):
        app = MDApp.get_running_app()
        app.store = store
        print("Event: on_cart_update Total " ,len(store)," items are in the cart." );

    def on_cart_request(self, item):
        print("Event: on_cart_request " ,item.name, "is added to the cart.");