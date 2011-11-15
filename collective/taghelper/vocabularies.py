from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary

from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from collective.taghelper.interfaces import ITagHelperSettingsSchema


def tagging_vocabulary_factory(context):
    items = []
    try:
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ITagHelperSettingsSchema)

        if settings.alchemy_api_key:
            items.append(('alchemy','AlchemyAPI'))
        if settings.yahoo_api_key:
            items.append(('yahoo','Yahoo'))
        if settings.calais_api_key:
            items.append(('calais','Open Calais'))
        items.append(('ttn','TagThe.Net'))
        items.append(('silcc','SiLLC'))
        return SimpleVocabulary.fromItems(items)
    except KeyError:
        return SimpleVocabulary.fromItems([])
