import re

from box import Box

from dom import dom

class dom(dict):
    def __int__(self,docStr):
        html = Box()
        tokens = dom.__tokenizer(docStr)
        for index, tkn in enumerate(tokens):
            str = ''
            count = 0
            start_Tag = None
            if dom.__isStartTag(tkn):
                list = self.__tokens[index:]
                start_Tag = re.sub('<','', tkn)

                for innerIndex, item in enumerate(list):
                    if dom.__isStartTag(item):
                        str = str + " " * count + item + '\n'
                        count = count + 1
                    elif dom.__isEndTag(item):
                        count = count - 1
                        str = str + " " * count + item + '\n'
                    else:
                        str = str + " " * count + item + '\n'
                    if not count:
                        if start_Tag not in html:
                            str = dom.__tag(str)

                            list = re.findall('<' + str['name'] + '[\s\S]*?' + str['name'] + '>', self.__htmlStr)
                            if len(list) > 1:
                                str.setdefault("all", list)

                            html.setdefault(start_Tag, str)
                            str = ''
                            start_Tag = None
                            break
                    elif innerIndex == len(list) - 1:
                        if start_Tag not in html:
                            str = dom.__tag(str)

                            list = re.findall('<' + str['name'] + '[\s\S]*?' + str['name'] + '>', self.__htmlStr)
                            if len(list) > 1:
                                str.setdefault("all", list)

                            html.setdefault(start_Tag, str)
                            str = ''
                            start_Tag = None

        self.update(html)


    def __getattr__(self, item):
        if self[item]:
            return self[item]
        else:
            return item + " not exist"


    def __tag(str):
        name = re.search('<\w+', str).group()[1:]
        dict = {}
        text = re.sub('<[^>]+>', '', str)
        startTag = re.search('<[^>]*>', str).group()

        pat = '(<' + name + '.*?>)|(</' + name + '?>)'
        content = re.subn(pat, '', str, 2)


        dict.setdefault("name", name)
        dict.setdefault("text", text)
        dict.setdefault("content", content[0])
        dict.setdefault("tag", str)
        attr = re.findall('\w+=".*?"', startTag)
        for i in attr:
            k, v = re.split('=', i)
            if k == "class":
                vlist = re.split(' ', v.strip('"'))

                dict.setdefault(k, vlist)
            dict.setdefault(k, v.strip('"'))

        return dict


    def __tokenizer(htmlStr):
        temp = re.sub('\n', '', htmlStr)
        temp = re.split('(<[^>]*>)', temp)
        temp = list(filter(lambda x: (x is not '' and x is not '\n'), temp))
        tmp = []
        for x in temp:
            tmp.append(x.strip())
        del(temp)
        return tmp

    def prettify(self):
        count = 0
        prettyText = ''
        selfClosingTag = ['<area />', '<base />', '<br />', '<embed />', '<hr />', '<iframe />', '<img />', '<input />',
                          '<link />', '<meta />', '<param />', '<source />', '<track />',
                          '<area>', '<base>', '<br>', '<embed>', '<hr>', '<iframe>', '<img>', '<input>',
                          '<link>', '<meta>', '<param>', '<source>', '<track>']

        for token in self.__tokens:

            if dom.__isStartTag(token):
                prettyText = prettyText + count * ' ' + token + '\n'
                count = count+1
            elif dom.__isEndTag(token) and token not in selfClosingTag:
                count = count-1
                prettyText = prettyText + count * ' ' + token + '\n'
            else:
                prettyText = prettyText + count * ' ' + token + '\n'
        return prettyText[0:len(prettyText)-1]



    def __isEndTag(token):
        if (re.match('</[A-Za-z]+', token)):
            return True
        return False

    def __isStartTag(token):
        selfClosingTag = ['<area />', '<base />', '<br />', '<embed />', '<hr />', '<iframe />', '<img />', '<input />',
                          '<link />', '<meta />', '<param />', '<source />', '<track />',
                          '<area>', '<base>', '<br>', '<embed>', '<hr>', '<iframe>', '<img>', '<input>',
                          '<link>', '<meta>', '<param>', '<source>', '<track>']

        if re.match('<[A-Za-z]+', token) and token not in selfClosingTag:
            return True
        return False
