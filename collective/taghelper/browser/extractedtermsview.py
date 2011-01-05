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
        elif self.context.portal_type == 'Link':
            self.url = self.context.getRemoteUrl()
        else:
            self.url = self.request.URL1 +'?ajax_load=1'
        self.text = self._get_text()

    def _get_text(self):
        portal_transforms = getToolByName(self.context, 'portal_transforms')
        text = ''
        if self.context.portal_type in ['Document', 'News Item', 'Event']:
            html = self.context.getText()
            text = portal_transforms.convert('html_to_text', html).getData()
            text = self.context.Title() + '. ' +\
                self.context.Description() +'. ' + text
        elif self.context.portal_type == 'Link':
            text = self.context.Title() + '. ' + self.context.Description()
        elif self.context.portal_type == 'File':
            try:
                text = portal_transforms.convertTo('text/plain',
                    self.context.data,
                    mimetype=self.context.get_content_type).getData()
            except AttributeError:
                pass
        elif self.context.portal_type == 'Project':
            html = self.context.getProject_summary()
            text = portal_transforms.convert('html_to_text', html).getData()
            text = self.context.Title() + '. ' +\
                self.context.Description() +'. ' + text
        return text


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
