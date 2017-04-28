import sys
import re

#Rule Based informal to formal Korean Translator

BASE_CODE, CHOSUNG, JUNGSUNG = 44032, 588, 28
CHOSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
JUNGSUNG_LIST = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']
JONGSUNG_LIST = [' ', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']

replaceDict = dict()

#path to data files
mypath = ''

#populate noun translation dict from file
def populateDictionary():
    fDictRead = open(mypath+'nounConjugation.txt','r',encoding="utf8")
    fDictReadLines = fDictRead.readlines()
    for it2 in range(0, len(fDictReadLines)):
        line = fDictReadLines[it2].replace('\n','').replace('\ufeff','').split(':')
        replaceDict[str(line[0])] = str(line[1])
    fDictRead.close()

#returns the "jongsung" of a given char
def getJongSung(char):
    if re.match('.*[ㄱ-ㅎㅏ-ㅣ가-힣]+.*', char) is not None:
        char_code = ord(char) - BASE_CODE
        char1 = int(char_code / CHOSUNG)
        char2 = int((char_code - (CHOSUNG * char1)) / JUNGSUNG)
        char3 = int((char_code - (CHOSUNG * char1) - (JUNGSUNG * char2)))
        return JONGSUNG_LIST[char3]

#apply verb conjugation
def conjugateVerbs(sentence):
    words = sentence.split()
    newWord = ''
    for word in words:
        wlen = len(word)
        #Check if verb (is end of sentence or has punctuation after)
        #padding is for retaining punctuation
        if (word[wlen - 1] in ['!', '.', '?']):
            isVerb = True
            padding = 0
        elif (words.index(word) == len(words)-1):
            isVerb = True
            padding = 1
        else:
            isVerb = False
        #Conjugate
        if(isVerb):
            conjugated = True
            #and statement checks if word is already formal
            if(word[wlen-2+padding] == '다' and word[wlen-3+padding]!='니'):
                #받침 있는 케이스
                if(getJongSung(word[wlen-3+padding]) != ' ' and getJongSung(word[wlen-3+padding]) !='ㄴ'):
                    newWord = word[:-2+padding] + "습니다"
                #ㄴ 받침 케이스
                elif(getJongSung(word[wlen-3+padding]) == 'ㄴ'):
                    #e.g. 않는다
                    if(word[wlen-3+padding]=='는'):
                        newWord = word[:-3 + padding] + '습니다'
                    else:#받침 ㄴ->ㅂ unicode +13
                        newWord = word[:-3 + padding] + chr(ord(word[wlen - 3 + padding]) + 13) + '니다'
                else:#노 받침 -> ㅂ unicode +17
                    newWord = word[:-3+padding] + chr(ord(word[wlen-3+padding])+17) + '니다'
            elif (word[wlen-2+padding] == '라'):
                newWord = word[:-2+padding] + "주세요"
            #걍 '요' 갖다 붙이면 되는 케이스
            elif (word[wlen-2+padding] in ['아','래','해','왜','마','려','군','가','고','돼','어'] ):
                if (padding == 0):
                    #remove punctuation before adding '요'
                    newWord = word[:-1] + "요"
                else:
                    newWord = word + "요"
            else:
                conjugated = False
            #add punctuation and replace informal verb with conjugated formal verb
            if(conjugated):
                if (padding == 0):
                    newWord += word[wlen - 1]
                sentence = sentence.replace(word, newWord)
    return sentence

#Replace sentence words existing in dictionary with values
def replaceWords(sentence):
    words = re.split(',|;| |!|#|%|&|\\?', sentence)
    for word in words:
        word = word.strip()
        if word in replaceDict:
            sentence = sentence.replace(word, replaceDict[word])
    return sentence

fread = open(mypath+'paired_data.txt','r',encoding="utf8")
#fread = open(mypath+'test.txt','r',encoding="utf8")
fwrite = open(mypath+'ruleBasedFormal.txt','w',encoding="utf8")

freadLines = fread.readlines()
populateDictionary()

for it in range(0, len(freadLines)):
    sentence = replaceWords(freadLines[it])
    sentence = conjugateVerbs(sentence)
    fwrite.write(sentence)
fread.close()
fwrite.close()