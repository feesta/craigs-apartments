craigs-apartments
=================

This is a quick and dirty web app/python server for tracking and sorting geotagged, Craigslist listings on a map. It consumes entries from the RSS feed for San Francisco, pulls out the important details, and puts the most recent 300 on a map. Sliders for time and price allow you to narrow your search. This is my desperation of apartment hunting in SF right now.


Dependancies: tornado, mongodb, beautifulsoup, feedparser, and leaflet

Crontab: <em>5,20,35,50 *  *   *   *    python run.py --price --grab --location --thumb</em>

Run: <em>python webserver.py</em>

View: <em>http://yourhost.com:8889/static/map.html</em>


<img src='http://farm8.staticflickr.com/7380/10180137423_25a41f5c06_o.png'>
