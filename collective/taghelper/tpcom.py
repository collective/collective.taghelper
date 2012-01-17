#call http://text-processing.com/ webservices
import urllib, urllib2
try:
    import simplejson as json
except ImportError:
    import json


class TextProcessing(object):
    url = 'http://text-processing.com/api/'

    result_keys = ['GSP', 'PP', 'FACILITY', 'GPE', 'PERCENT', 'NP',
        'VP', 'PERSON', 'DURATION', 'CARDINAL', 'LOCATION', 'MEASURE',
        'DATE', 'ORGANIZATION']

    def __init__(self):
        pass

    def _analyze(self, text, service='tag'):
        params = urllib.urlencode({'text':text[:9999]})
        url = self.url + service + '/'
        result = json.load(urllib2.urlopen(url, data=params))
        prefered_keys = ['FACILITY','ORGANIZATION']
        results =[]
        for k,v in result.iteritems():
            if k in prefered_keys:
                results += v
        return results

    def tag(self, text):
        '''
        curl -d "text=California is nice" http://text-processing.com/api/tag/
        '''
        self._analyze(text, 'tag')


    def analyze(self,text):
        '''
        curl -d "text=California is nice" http://text-processing.com/api/phrases/
        '''
        return self._analyze(text, 'phrases')
