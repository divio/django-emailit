# -*- coding: utf-8 -*-
from django.utils import translation


class force_language:
    def __init__(self, new_lang):
        self.new_lang = new_lang
        self.old_lang = translation.get_language()
    def __enter__(self):
       translation.activate(self.new_lang)
    def __exit__(self, type, value, tb):
       translation.activate(self.old_lang)