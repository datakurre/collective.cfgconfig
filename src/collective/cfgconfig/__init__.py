# -*- coding: utf-8 -*-
import imp
import os
import sys
from pkgutil import ImpLoader


def processcfgfile(file, context, testing=False):
    """Patch zope.configuration.xmlconfig.processxmlfile with cfg support"""
    from zope.configuration.xmlconfig import _processxmlfile
    if file.name.endswith('.zcml'):
        return _processxmlfile(file, context, testing)

    import ConfigParser
    config = ConfigParser.RawConfigParser()
    config.readfp(file)

    for section in config.sections():
        name = section.split(':')[:-1]
        if len(name) == 1:
            name = ['http://namespaces.zope.org/zope', name[0]]
        else:
            name[0] = 'http://namespaces.zope.org/' + name[0]
        data = dict(config.items(section))
        context.begin(tuple(name), data)
        context.end()


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
                    processcfgfile)
            return '<component></component>'
        return super(MonkeyPatcher, self).get_data(self, pathname)

__loader__ = MonkeyPatcher(sys.modules[__name__])
