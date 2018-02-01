# -*- coding: utf-8 -*-
from django.conf import settings
from django.utils import translation


class force_language:
    def __init__(self, new_lang):
        self.new_lang = new_lang
        self.old_lang = translation.get_language()

    def __enter__(self):
        translation.activate(self.new_lang)

    def __exit__(self, type, value, tb):
        translation.activate(self.old_lang)


def get_template_name(language, base, part, suffix):
    if language:
        return u'.'.join((base, part, language, suffix))
    else:
        return u'.'.join((base, part, suffix))


def get_template_names(language, base, part, suffix):
    template_names = [
        get_template_name(language, base, part, suffix),
        get_template_name(None, base, part, suffix),
    ]
    for lang, lang_name in settings.LANGUAGES:
        if not lang == language:
            template_names.append(get_template_name(lang, base, part, suffix))
    return template_names
