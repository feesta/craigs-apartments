craigs-apartments
=================

Quick and dirty web app/python server for tracking and sorting geotagged Craigslist listings on a map.

Crontab: <em>5,20,35,50 *  *   *   *    python run.py --price --grab --location --thumb</em>

Run: <em>python webserver.py</em>

View: <em>http://yourhost.com:8889/static/map.html</em>

Uses tornado, mongo, beautifulsoup, feedparser, and leaflet

<img src='http://farm8.staticflickr.com/7380/10180137423_25a41f5c06_o.png'>
