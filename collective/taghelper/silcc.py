import urllib, urllib2


class Silcc(object):

    api_key = None
    url = 'http://opensilcc.com/api/tag'

    def __init__(self, api_key, url="http://opensilcc.com/api/tag"):
        self.api_key = api_key
        self.url = url

    def rest_POST(self, content):
        params = urllib.urlencode({'key': self.api_key, 'text': content})
        response = urllib2.urlopen(self.url, data=params)
        data = response.read()
        return (data)

    def execute(self, content):
        if not (content and  len(content.strip())):
            return None
        result = self.rest_POST(content)
        results = [r.strip('"') for r in result[1:-1].split(', ')]
        return results
