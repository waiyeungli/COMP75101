from kivy.uix.recycleview import RecycleView
from event import getEvent

class ExploreScreen(RecycleView):
    def __init__(self, **kwargs):
        ev = getEvent()
        ev.bind(on_product_update=self.fillExploreScreen)
        super(ExploreScreen, self).__init__(**kwargs)

    def fillExploreScreen(self, event, store):
        keys = list(store.keys())
        size = len(keys)
        self.data = [{'key':keys[id % size], 'img': store[keys[id % size]]['images'][0], 'name':store[keys[id % size]]['name'], 'price':str(
            store[keys[id % size]]['price']), 'description':store[keys[id % size]]['description']} for id in range(500)]