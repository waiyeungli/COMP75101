from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import  Screen

from index import ProductCarouselImage
from index import ProductGridImage
from index import ProductListItem
from event import getEvent
#from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty


Window.size = (400, 800)
Window.maximum_width = 700  # This seems not working


class HomeScreen(Screen):
    isSearching = NumericProperty(0)

    def __init__(self, **kwargs):
        print('binding on product update event')
        ev = getEvent()
        ev.bind(on_product_update=self.fillCarousel)
        ev.bind(on_product_update=self.fillTopDeal)
        ev.bind(on_product_update=self.fillFreeShipping)
        ev.bind(on_product_update=self.fillRecommend)
        ev.bind(on_product_update=self.fillWishList)
        super(HomeScreen, self).__init__(**kwargs)

    def on_text_change(self, text):
        self.isSearching = max(0,len(text)-1)
        # TODO: filter the result

        app = MDApp.get_running_app()
        if self.isSearching:
            # temp = len(self.ids.search_result.children)
            self.ids.search_result.clear_widgets()
            for k in app.display_store:
                if text.lower() in app.display_store[k]["name"].lower() or text.lower() in app.display_store[k]["category"].lower() or text.lower() in app.display_store[k]["description"].lower():
                    self.ids.search_result.add_widget(
                        ProductListItem(item=app.display_store[k]))

    def fillCarousel(self, event, display_store):
        byCategory = sorted(display_store, key=lambda x: display_store[x]["category"])
        for k in byCategory[:8]:
            self.ids.carousel.add_widget(
                ProductCarouselImage(source="image/"+display_store[k]['images'][0],item=display_store[k]))

    def fillTopDeal(self, event, display_store):
        cheapest = sorted(display_store, key=lambda x: float(display_store[x]["price"]))
        for k in cheapest[:4]:
            self.ids.top_deal.add_widget(
                ProductGridImage(source="image/"+display_store[k]['images'][0],item=display_store[k]))
        self.ids.top_deal.do_layout()

    def fillFreeShipping(self, event, display_store):
        byName = sorted(display_store, key=lambda x: display_store[x]["name"], reverse=True)
        for k in byName[:4]:
            self.ids.free_shipping.add_widget(ProductListItem(item=display_store[k]))

    def fillRecommend(self, event, display_store):
        byName = sorted(display_store, key=lambda x: display_store[x]["name"])
        for k in byName[:4]:
            self.ids.recommend.add_widget(ProductListItem(item=display_store[k]))

    def fillWishList(self, event, display_store):
        byName = sorted(display_store, key=lambda x: float(display_store[x]["price"]), reverse=True)
        for k in byName[:4]:
            # print(item["name"],item["price"],item['images'][0])
            #print(store[k]["price"])
            self.ids.wish_list.add_widget(ProductListItem(item=display_store[k]))
