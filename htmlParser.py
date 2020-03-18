

from box import Box



html_doc = """
<head>
<Title>The Dormouse's story</Title>
</head>
<body>
<p class="title para"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">..a.</p>

"""
html = """
<html>

<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
</body>
</html>
"""

import re
selfClosingTag = ['<area />','<base />','<br />','<embed />','<hr />', '<iframe />', '<img />','<input />','<link />','<meta />','<param />','<source />','<track />',
                  '<area>', '<base>', '<br>', '<embed>', '<hr>', '<iframe>', '<img>', '<input>',
                  '<link>', '<meta>', '<param>', '<source>', '<track>']


#
# def isTag(token):
#      if(re.match('<[A-Za-z]+', token) or re.match('</[A-Za-z]+', token)):
#         return True
#      return False
#
#
# def __isStartTag(token):
#     if (re.match('<[A-Za-z]+', token)):
#         return True
#     return False
# pre___tokens = {"body" :[ {"p": "hello", "style":"bold" },{"p": "world", "style":"normal"}]}
#

class htmlParser(dict):

    def __init__(self,htmlStr):


        self.__htmlStr = htmlStr
        self.__tokens = htmlParser.__tokenizer(htmlStr)
        # self.title = title(htmlStr)
        # self.p = p(htmlStr)
        # self.a = a(htmlStr)
        html = Box()
        for index,tkn in enumerate(self.__tokens):
            str = ''
            count = 0
            start_Tag = None
            if htmlParser.__isStartTag(tkn):
                list = self.__tokens[index:]
                start_Tag = re.match('<\w+',tkn).group()[1:]

                for innerIndex, item in enumerate(list):
                    if htmlParser.__isStartTag(item):
                        str = str + " " * count + item + '\n'
                        count = count + 1
                    elif htmlParser.__isEndTag(item):
                        count = count - 1
                        str = str + " "*count +item+'\n'
                    else:
                        str = str + " "*count +item+'\n'
                    if not count:
                        if start_Tag not in html:
                            str = htmlParser.__tag(str)

                            list = re.findall('<'+str['name']+'[\s\S]*?'+str['name']+'>', self.__htmlStr)
                            if len(list) > 1:
                                str.setdefault("all",list)

                            html.setdefault(start_Tag,str)
                            str = ''
                            start_Tag = None
                            break
                    elif innerIndex == len(list)-1:
                        if start_Tag not in html:
                            str = htmlParser.__tag(str)

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

            if htmlParser.__isStartTag(token):
                prettyText = prettyText + count * ' ' + token + '\n'
                count = count+1
            elif htmlParser.__isEndTag(token) and token not in selfClosingTag:
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

    def selector(self,tag_name):
            tag = self[tag_name]
            # def get(attr):
            #    return self[tag_name][attr]
            # tag["get"] = get
            return tag



    def find(self,tag_name):
        return self[tag_name].tag

    def findAll(self,tag_name):
        return self[tag_name].all






#
# h = htmlParser(html_doc)
# print(h.head)
#










