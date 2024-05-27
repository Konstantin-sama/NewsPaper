from django import template

register = template.Library()


@register.filter(name='Censor')
def Censor(value):
    Banned_List = ['idiot', 'stupid', 'donkey', 'Stupid', 'редиска', 'Редиска']
    sentence = value.split()
    for i in Banned_List:
        for words in sentence:
            if i in words:
                news = sentence.index(words)
                sentence.remove(words)
                sentence.insert(news, '*' * len(i))
    return " ".join(sentence)

    # def hide_forbidden(value):
    #     words = value.split()
    #     result = []
    #     for word in words:
    #         if word in Banned_List:
    #             result.append(word[0] + "*"*(len(word)-2) + word[-1])
    #         else:
    #             result.append(word)
