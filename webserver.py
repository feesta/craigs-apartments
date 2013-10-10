import os.path, time
import tornado.ioloop, tornado.web
from tornado import autoreload, websocket
import simplejson as json
import pymongo
from bson import objectid
import requests


connection = pymongo.Connection("localhost", 27017) 
db = connection.craig

class SlashHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

class ListHandler(tornado.web.RequestHandler):
    def get(self):
        obj = []
        for entry in db.entries.find().sort("_id",-1).limit(300):
            #self.write(entry['url'])
            #self.write("<br>")
            if 'latlng' not in entry: continue
            if 'price' not in entry: continue
            if 'images' not in entry: continue
            ee = {'latlng':entry['latlng'], 
                  'url':entry['url'],
                  'title':entry['rss_entry']['title'],
                  'price':entry['price'],
                  'images':entry['images'],
                  'timestamp':time.mktime(objectid.ObjectId(entry['_id']).generation_time.timetuple())
            }
            obj.append(ee)
        self.write(json.dumps(obj))



application = tornado.web.Application([
        (r"/(favicon\.ico)", tornado.web.StaticFileHandler, {"path": "static"}),
        (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": "static"}),
        (r"/", SlashHandler),
        (r"/list", ListHandler),
    ], 
    debug=True, 
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
)

if __name__ == "__main__":
    application.listen(8889)
    ioloop = tornado.ioloop.IOLoop.instance()
    autoreload.start(ioloop)
    ioloop.start()
