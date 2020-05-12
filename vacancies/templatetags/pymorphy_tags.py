import pymorphy2

from django import template


morph = pymorphy2.MorphAnalyzer()
register = template.Library()


def pluralize_word(word, number):
    # https://pymorphy2.readthedocs.io/en/latest/user/guide.html

    parsed = morph.parse(word)[0]
    pluralized = parsed.make_agree_with_number(number)
    if pluralized is not None:
        return pluralized.word

    return word


@register.filter
def plural(word, number):
    if not word or not number:
        return word
    return pluralize_word(word, number)
