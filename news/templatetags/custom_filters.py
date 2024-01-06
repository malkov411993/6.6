from django import template


register = template.Library()


@register.filter()
def censor(text):
    list_words = text.split()
    censor_words = {'революция', 'психологию', 'психология', 'роль', }
    censor_text = []
    # если text строка, то условие выполняется
    if isinstance(text, str):
        for word in list_words:
            if word.lower() in censor_words:
                word = f'{word[0]}{"*" * (len(word) - 2)}{word[-1]}'
            censor_text.append(word)
        return ' '.join(censor_text)

