#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import utilities
import feedparser
from BeautifulSoup import BeautifulSoup
import pymongo, bson
import argparse
import re

url = "http://sfbay.craigslist.org/search/apa/sfc?maxAsk=6000&minAsk=1000&format=rss"

connection = pymongo.Connection("localhost", 27017) 
db = connection.craig
geodb = connection.geodb

def get_entries():
    feed = feedparser.parse(url)

    cc = 0
    for entry in feed['entries']:
        entry_url = entry['link']
        row = db.entries.find_one({'url':entry_url})
        if not row:
            raw = utilities.downloadURL(entry_url)
            print entry_url
            raw = raw.decode('cp1252')
            if raw is None:
                print "failed to download..."
                raw = ''
            entry.pop('updated_parsed')
            entry.pop('published_parsed')
            db.entries.insert({'url':entry_url,
                             'html':raw,
                             'rss_entry':entry})
            cc += 1
            if cc > 10: break

def find_price():
    for entry in db.entries.find({'price':{'$exists':False}}):
        title = entry['rss_entry']['title']
        m = re.search('\$[0-9,]+',title)
        try:
            price = int(re.sub('\$|,','',m.group(0)))
            print "$%s" % price
            db.entries.update({'_id':entry['_id']},
                              {'$set':{'price':price}})
        except:
            print title

def find_location():
    for entry in db.entries.find({'latlng':{'$exists':False}}):
        html = entry['html']
        soup = BeautifulSoup(html)
        map_div = soup.find("div", {"id": "map"})
        if map_div is not None:
            lat = map_div['data-latitude']
            lng = map_div['data-longitude']
            print "%s, %s" % (lat, lng)
            db.entries.update({'_id':entry['_id']},
                              {'$set':{'latlng':{'lat':lat,'lng':lng}}})

def find_thumb():
    for entry in db.entries.find({'images':{'$exists':False}}).limit(500):
        html = entry['html']
        soup = BeautifulSoup(html)
        thumb_div = soup.find("div", {"id": "thumbs"})
        #print thumb_div
        if thumb_div is not None:
            a = thumb_div.find("a")
            img = thumb_div.find("img")
            fullsize = a['href']
            thumb = img['src']
            print thumb
            db.entries.update({'_id':entry['_id']},
                              {'$set':{'images':{'fullsize':fullsize,'thumb':thumb}}})

#print utilities.geocodeLocation("1000 van ness ave", geodb.geocode)
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--grab", help="get entries from Craig",
                        action="store_true")
    parser.add_argument("--price", help="get entries from Craig",
                        action="store_true")
    parser.add_argument("--location", help="get location from Craig",
                        action="store_true")
    parser.add_argument("--thumb", help="get thumb from Craig",
                        action="store_true")
    args = parser.parse_args()
    if args.grab:
        get_entries()
    if args.location:
        find_location()
    if args.price:
        find_price()
    if args.thumb:
        find_thumb()
    pass
