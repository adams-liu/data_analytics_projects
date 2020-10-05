import re
word = 'professional experience with .net core, azure sql db, javascript and html development'


print(re.findall('java'+'\\b', word))