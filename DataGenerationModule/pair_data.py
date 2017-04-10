'''
Create Paired data using formal
'''

import codecs

def readFile(filename_informal, filename_formal):

    f_informal = codecs.open(filename_informal, encoding = "utf-8",  mode = "r")
    f_formal = codecs.open(filename_formal,encoding = "utf-8", mode="r")
    foutput = codecs.open("output_pair.txt", encoding = "utf-8", mode="w")
    while True:
        formal = f_formal.readline()
        informal = f_informal.readline()

        if not formal or not informal: break
        foutput.write(informal.strip()+":"+formal)

readFile("korean_informal.txt","korean_formal.txt")