# -*- coding: utf-8 -*-

from Products.Five.browser import BrowserView


class HelloWorld(BrowserView):

    def __call__(self):
        return u"Hello world"
