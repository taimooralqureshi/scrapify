from htmlParser import htmlParser

html_doc = """
<html>
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
</html>
"""

print( '===parse object===')
# dom object
dom = htmlParser(html_doc)
print(dom)
print('='*100)


print("===General/Primary Attributes===")

#<<<two type of access attr>>>

# selecting p tag for demo purpose
# p object
print(dom.p)
print(dom['p'])
print('-'*60)


# p name attribute
# show which actually we accessing
print(dom.p.name)
print(dom.p['name'])
print('-'*60)


# p text attr
# get the only text inside tag or nested tag
print(dom.p.text)
print('-'*60)


# p content attr
# content contain inside tag may be it can be text or nested tag
print(dom.p['content'])
print('-'*60)


# p tag attr
# complete picture of tag
print(dom.p.tag)
print('-'*60)


print("===Specific/Secondary Attributes===")
# these attribute only specific to tag


# class attr of p tag
# here two way access attr is actually beneficial
print(dom.p.Class) # class is keyword can't use to access attr
print(dom.p['class'])

print(dom.p['class'][1])
print('-'*60)


# attrs of anchor tag
print(dom.a.tag)
print('-'*60)

print(dom.a.href)
print(dom.a.id)
print(dom.a['class'])
print('-'*60)

# list of all occurance of tag
for a in dom.a.all:
    print(a)
print('-'*60)


#now the top of that we can build web scraping package
print(dom.prettify())
print('-'*60)


print(dom.selector('a'))
print(dom.selector('a').get('class'))
print(dom.selector('a').get('href'))
print('-'*60)


print(dom.find('a'))
print('-'*60)


print(dom.findAll('a'))
print('-'*60)





