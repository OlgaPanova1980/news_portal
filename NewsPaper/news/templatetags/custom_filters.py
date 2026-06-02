from django import template

register = template.Library()

FORBIDDEN_WORDS = ['редиска', 'дурак', 'плохоеслово']


@register.filter()
def censor(value):
    if not isinstance(value, str):
        raise ValueError("Фильтр censor можно применять только к строкам!")

    text = value
    for word in FORBIDDEN_WORDS:
        if word.lower() in text.lower():
            censored = word[0] + '*' * (len(word) - 1)
            text = text.replace(word, censored)

    return text