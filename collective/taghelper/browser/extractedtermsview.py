from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

from collective.taghelper import taghelperMessageFactory as _
from collective.taghelper.utilities import get_yql_subjects
from collective.taghelper.utilities import get_calais_subjects
from collective.taghelper.utilities import get_silcc_subjects
from collective.taghelper.utilities import get_ttn_subjects


class IExtractedTermsView(Interface):
    """
    ExtractedTerms view interface
    """




class ExtractedTermsView(BrowserView):
    """
    ExtractedTerms browser view
    """
    implements(IExtractedTermsView)

    template = ViewPageTemplateFile('extractedtermsview.pt')

    def __init__(self, context, request):
        self.context = context
        self.request = request
        if self.context.portal_type == 'File':
            self.url = self.request.URL1 +'/filehtmlpreview_view'
        elif hasattr(self.context, 'getRemoteUrl'):
            self.url = self.context.getRemoteUrl()
        if not self.url:
            self.url = self.request.URL1 +'?ajax_load=1'
        self.text = self._get_text()

    def _get_text(self):
        if hasattr(self.context, 'SearchableText'):
            return self.context.SearchableText()
        else:
            return ''


    def yahoo_terms(self):
        return get_yql_subjects(self.url)

    def calais_terms(self):
        return get_calais_subjects(self.text, self.context.UID())

    def ttn_terms(self):
        return get_ttn_subjects(self.text)


    def silcc_terms(self):
        text = self.context.Title() + '. ' + self.context.Description()
        return get_silcc_subjects(text)

    def __call__(self):
        form = self.request.form
        if form.has_key('form.button.save'):
            keywords = list(self.context.Subject())
            keywords = keywords + form.get('subject', [])
            keywords=list(set(keywords))
            self.context.setSubject(keywords)
            self.request.response.redirect(self.context.absolute_url() + '/edit')
            return ''
        elif form.has_key('form.button.cancel'):
            self.request.response.redirect(self.context.absolute_url() + '/view')
            return ''
        return self.template()
