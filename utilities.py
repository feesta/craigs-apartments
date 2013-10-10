import urllib2, cookielib, socket
from httplib import BadStatusLine, InvalidURL
import json, time, sys
import pymongo

socket.setdefaulttimeout(30)

def downloadURL(url):
    """Downloads the URL.
    """
    try:
        cj = cookielib.CookieJar()
        cp = urllib2.HTTPCookieProcessor(cj)
        opener = urllib2.build_opener(cp)
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        request = urllib2.Request(url)
        u = opener.open(request)
        raw_text = u.read()
        return raw_text
    except urllib2.URLError:
        print "URLError: %s" % url
        return None
    except (urllib2.HTTPError, BadStatusLine, InvalidURL):
        print "HTTPError: %s" % (url)
        return None
    except (socket.timeout):
        print "Timeout: %s" % url
        return None
    except Exception as e:
        print "Error: %s" % url
        print e
        return None
    
def getRedirectedURL(url):
    """Gets the redirected URL.
    """
    try:
        cj = cookielib.CookieJar()
        cp = urllib2.HTTPCookieProcessor(cj)
        opener = urllib2.build_opener(cp)
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        url = url.replace('^https', 'http')
        request = urllib2.Request(url)
        u = opener.open(request)
        redirected_url = u.geturl()
        return redirected_url
    except urllib2.URLError:
        print "URLError: %s" % url
        return None
    except (urllib2.HTTPError, BadStatusLine, InvalidURL):
        print "HTTPError: %s" % (url)
        return None
    except (socket.timeout):
        print "Timeout: %s" % url
        return None
    except Exception as e:
        print "Error: %s" % url
        print e
        return None

def removekey(d, key):
    r = dict(d)
    del r[key]
    return r

def decodeUrl(url):
    url_decoded = urllib2.unquote(url).decode('utf-8')
    return url_decoded
def encodeUrl(url):
    url_encoded = urllib2.quote(url.encode('utf-8'))
    return url_encoded

def geocodeLocations(locations):
    """Uses the OSM Nominatim (hosted by Mapquest Open) to find the location for an array of strings.
       However, if one is bad/non-existent, it seems the whole query fails.
    """
    maxResults = 1
    location_query = ''
    for location in locations:
        location_query += "&location=%s" % encodeUrl(location)
    url = "http://open.mapquestapi.com/geocoding/v1/batch?maxResults=%d%s" % (maxResults, location_query)
    print url
    results = json.loads(urllib2.urlopen(url).read())
    print results
    return
    for location_result in results['results']:
        #print location_result
        if location_result['providedLocation']['location'] == location:
            latlng = location_result['locations'][0]['displayLatLng']
            return latlng
        else:
            print location_result




def geocodeLocation(location, geocodeDB, tries=0):
    """Uses the OSM Nominatim (hosted by Mapquest Open) to find the location for a string
    """
    try:
        location = encodeUrl(location)
    except UnicodeDecodeError:
        pass

    try:
        row = geocodeDB.find_one({'query':location})
    except:
        row = None
    if row:
        print 'Cached. Times: {%d}' % row['count']
        results = row['results']
        geocodeDB.update({'_id':row['_id']}, {'$inc':{'count':1}})
    else:
        url = "http://open.mapquestapi.com/nominatim/v1/search?format=json&addressdetails=0&bounded=1&viewbox=-123.173825,37.9298443,-122.28178,37.63983&q=%s" % location
        print url
        try:
            results = json.loads(urllib2.urlopen(url).read())
            print results
        except (socket.timeout, socket.error):
            print 'failed to get: %s' % url
            #print 'socket.timeout so waiting a few seconds before trying again'
            if tries >= 3:
                geocodeDB.save({'query':location, 'results':None, 'count':1})
                return None
            else:
                for i in range(5):
                    sys.stdout.write('    %d seconds left\r' % (5 - i))
                    sys.stdout.flush()
                    time.sleep(1)
                print 'continuing...'
                return geocodeLocation(location, geocodeDB, tries+1)
                #return None
        except urllib2.URLError:
            print "URLError"
            return None
        geocodeDB.save({'query':location, 'results':results, 'count':1})
    if results:
        for obj in results:
            return {'lat':obj['lat'], 'lon':obj['lon']}
    else:
        print "no results for: %s", location
        return None



if __name__ == "__main__":
    url = getRedirectedURL('http://bit.ly/15g7P5t')
    print url
    print decodeUrl(url)
    print encodeUrl(url)
    print encodeUrl('http://vast-ravine-6427.herokuapp.com/?lat=37.7&lon=-122.4')
    pass

