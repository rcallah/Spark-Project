#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
'''
Python Version: 2.7.5 (default, Mar  9 2014, 22:15:05) 
[GCC 4.2.1 Compatible Apple LLVM 5.0 (clang-500.0.68)]
JAR:stanford-ner/stanford-ner.jar
CLASSIFIER:stanford-ner/english.muc.7class.distsim.crf.ser.gz
The nltk version is 2.0.4.
The scikit-learn version is 0.15-git.
'''


import nltk
import re 


# searchConcordance function
#x = searchConcordance("evidence",items["text"].lower(),numBefore=5,numAfter=5, precise=True)

def searchConcordance(strText,fullText,numBefore,numAfter, precise):
    arrFullText =nltk.word_tokenize(fullText)
    returnArray = []
    reset_b = numBefore
    reset_a = numAfter
    for i, items in enumerate(arrFullText):
        numBefore=reset_b
        numAfter=reset_a
        if precise == False:
            if strText in items:
                if (i-numBefore)< 0:
                    numBefore=i
                if (i+numAfter)>len(arrFullText)-1:
                    numAfter = len(arrFullText)- i + 1
                returnArray.append(arrFullText[i-numBefore:i+numAfter+1])
        else:    
            if strText==items:
                if (i-numBefore)< 0:
                    numBefore=i
                if (i+numAfter)>len(arrFullText)-1:
                    numAfter = len(arrFullText)- i + 1 
                returnArray.append(arrFullText[i-numBefore:i+numAfter+1])
    return returnArray




def encode(string):
        clean_sentence_unwantedchars= '["\t\n ]+'
        string = string.encode('utf8')
        string = string.decode('utf-8')    
        string = re.sub(clean_sentence_unwantedchars, ' ', string)
        string = string.encode('ascii', 'replace').encode('utf-8')
        string = string.decode('utf-8')
        return str(string)

