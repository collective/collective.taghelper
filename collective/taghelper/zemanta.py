import urllib, urllib2
try:
    import simplejson as json
except ImportError:
    import json

class Zemanta(object):

    api_key = None
    url = 'http://api.zemanta.com/services/rest/0.0/'

    def __init__(self, api_key):
        self.api_key = api_key

    def analyze(self, text, title=''):
        args = {'method': "zemanta.suggest",
        'api_key': self.api_key,
        'text': text.lstrip(title),
        'return_images': 0,
        'return_keywords': 1,
        'text_title': title,
        'images_limit': 0,
        'articles_limit': 0,
        'format': 'json'}
        args_enc = urllib.urlencode(args)
        raw_output = urllib.urlopen(self.url, args_enc).read()
        output = json.loads(raw_output)
        if output['status'].lower()=='ok':
            #XXX filter out only kw with 'relevance' > 0.5
            return [kw['name'] for kw in output['keywords']]
        return []
