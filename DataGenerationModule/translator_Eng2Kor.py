'''
Trnaslate English to Korean Using Goggle API
'''

from translate import Translator
import codecs

def write_to_file(file_name, res):
	with codecs.open(file_name, encoding='utf-8', mode='w+') as f:
		f.write(res)

t = Translator()
f = open("eng.txt","r")
fo = open("korean_formal.txt","w",encoding='utf-8')
while True:
    line = f.readline()
    if not line: break
    res = t.translate(line, from_lang='en', to_lang='ko')
    print(res)
    fo.write(res + "\n")