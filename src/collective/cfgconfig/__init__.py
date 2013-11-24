# -*- coding: utf-8 -*-
import imp
import os
import sys
from pkgutil import ImpLoader

NAMESPACES = {
    '': 'http://namespaces.zope.org/zope',
    'meta': 'http://namespaces.zope.org/meta',
    'zcml': 'http://namespaces.zope.org/zcml',
    'grok': 'http://namespaces.zope.org/grok',
    'browser': 'http://namespaces.zope.org/browser',
    'genericsetup': 'http://namespaces.zope.org/genericsetup',
    'i18n': 'http://namespaces.zope.org/i18n'
}


def processcfgfile(file, context, testing=False):
    """Process a configuration file (cfg)"""

    import ConfigParser
    config = ConfigParser.RawConfigParser()
    config.readfp(file)
    sections = config._sections

    # Define namespaces
    namespaces = NAMESPACES.copy()
    if 'namespaces' in sections:
        namespaces.update(config.items('namespaces'))
        sections.pop('namespaces', None)

    from zope.configuration.xmlconfig import ConfigurationHandler
    handler = ConfigurationHandler(context, testing=testing)

    # Read directives in resolved order
    for section in sections:
        # Read arguments
        data = sections.get(section, {})
        data.pop('__name__', None)

        # Resolve condition
        condition = data.pop('condition', None)
        if condition:
            if not handler.evaluateCondition(condition):
                continue

        # Resolve namespace and directive
        name = section.split(':')[:-1]
        if len(name) == 1:
            name = [namespaces[''], name[0]]
        else:
            name[0] = namespaces[name[0]]

        # Configure!
        context.begin(tuple(name), data)
        context.end()


def processxmlfile(file, context, testing=False):
    """Process a configuration file (either zcml or cfg)"""
    from zope.configuration.xmlconfig import _processxmlfile
    if file.name.endswith('.zcml'):
        return _processxmlfile(file, context, testing)
    else:
        return processcfgfile(file, context, testing)


class MonkeyPatcher(ImpLoader):
    """
    ZConfig uses PEP 302 module hooks to load this file, and this class
    implements a get_data hook to intercept the component.xml loading and give
    us a point to generate it.
    """
    def __init__(self, module):
        name = module.__name__
        path = os.path.dirname(module.__file__)
        description = ('', '', imp.PKG_DIRECTORY)
        ImpLoader.__init__(self, name, None, path, description)

    def get_data(self, pathname):
        if os.path.split(pathname) == (self.filename, 'component.xml'):
            import zope.configuration.xmlconfig
            setattr(zope.configuration.xmlconfig,
                    '_processxmlfile',
                    zope.configuration.xmlconfig.processxmlfile)
            setattr(zope.configuration.xmlconfig,
                    'processxmlfile',
                    processxmlfile)
            return '<component></component>'
        return super(MonkeyPatcher, self).get_data(self, pathname)

__loader__ = MonkeyPatcher(sys.modules[__name__])
